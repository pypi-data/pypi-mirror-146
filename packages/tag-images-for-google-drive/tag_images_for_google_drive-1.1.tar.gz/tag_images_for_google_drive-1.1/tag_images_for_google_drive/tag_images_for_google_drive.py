# -*- coding: utf-8 -*-
"""
Tools inject hashtag in file description and synchronize this tags in CSV file.
"""
import csv
import itertools
import logging
import shutil
import sys
from json import JSONDecodeError
from pathlib import Path
from typing import Dict, Tuple, Sequence, Optional, Mapping, AbstractSet, List, Set

import click
import click_pathlib

from tag_images_for_google_drive.exiftool import ExifTool
from tag_images_for_google_drive.tools import Glob, init_logger

LOGGER = logging.getLogger(__name__)

SEP = ","


def _set_tags(exif_tool: ExifTool, meta_info: Mapping[str, str], file: Path) -> None:
    """
       Set tags in file

       :param exif_tool: Exif tool wrapper
       :param meta_info: A dictionary of meta info
       :param file: The filename
    """
    params = ["-" + key + "=" + val for key, val in meta_info.items()]
    params.append("-overwrite_original")
    params.append("-sep")
    params.append(SEP)
    params.append("-photoshop:all=")
    params.append(str(file))
    try:
        exif_tool.execute(*params)
    except (UnicodeEncodeError, JSONDecodeError) as e:
        LOGGER.error(e)


def _purge_tags(tags: Sequence[str]) -> List[str]:
    """
       Purge tags. Remove duplicate and sort tags

       :param tags: A sequence of tags
       :return: purged tags
    """
    return sorted(set({key.strip().lower() for key in tags if key}))


def _extract_tags(description: str, separator: str) -> Tuple[str, List[str]]:
    """
       Extract tags. Extract Hashtag after the first '#'.

       :param description: A description with hashtag.
       :return: A tuple with only the description and a list of hashtag.
    """
    sp = description.split(separator)
    tags = list(itertools.chain(*[x.split(",") for x in sp[1:]]))
    tags = list(itertools.chain(*[x.split(";") for x in tags]))
    return sp[0].strip(), _purge_tags(tags)


def _extract_description(metadata: Mapping[str, str]) -> str:
    """
       Extract description from image file.

       :param metadata: Extracted meta-data from file.
       :return: The description
    """
    description = ""
    description = metadata.get("IPTC:Headline", description)
    description = metadata.get("EXIF:ImageDescription", description)
    description = metadata.get("IPTC:Caption-Abstract", description)
    description = metadata.get("PNG:Description", description)
    description = metadata.get("XMP:Description", description)
    description = metadata.get("PNG:Comment", description)
    description = metadata.get("File:Comment", description)
    description = metadata.get("Description", description)
    return description


def _extract_description_and_tags(exif_tool: ExifTool, file: Path) -> Tuple[bool, str, List[str]]:
    """
       Extract description and tags from image file.

       :param exif_tool: Exif tool wrapper
       :param file: The file path name.
       :return: A tuple with true if the must be updated, the description and all hashtags
    """
    metadata = exif_tool.get_tags(["Comment", "Description", "Caption-Abstract", "imageDescription", "Headline",
                                   "Keywords", "Subject"], str(file))
    # Extract description with hash tags
    description = _extract_description(metadata)

    # Extract keywords
    keywords, old_keywords = _extract_keywords(description, metadata)

    old_keywords = _purge_tags(old_keywords)
    keywords = _purge_tags(keywords)
    split = description.split('#')
    description = split[0]
    in_description = _purge_tags(split[1:])
    must_update = old_keywords != keywords or in_description != keywords
    return must_update, description.strip(), keywords


def _extract_keywords(description, metadata) -> Tuple[Sequence[str], Sequence[str]]:
    keywords: List[str] = []
    # Limit to 64 chars
    keywords = metadata.get("XMP:Subject")
    if not keywords:
        keys = ["IPTC:Keywords", "Keywords"]
        all_keywords: List[str] = []
        for key in keys:
            keywords = metadata.get(key, keywords)
            if isinstance(keywords, str):
                if len(keywords) < 63:  # I can trust the keywords tag
                    _, keywords = _extract_tags("," + keywords, ",")
                    keywords = keywords + _extract_tags(description, "#")[1]
                    old_keywords = keywords
                else:
                    keywords = _extract_tags(description, "#")[1]
                    keywords = [str(i) for i in keywords if i]  # Remove empty tags
                    old_keywords = keywords
            elif keywords:
                keywords = [str(key) for key in keywords]
                old_keywords = keywords
                keywords = keywords + _extract_tags(description, "#")[1]
            else:
                old_keywords = []
                keywords = _extract_tags(description, "#")[1]
            all_keywords += keywords
    else:
        if isinstance(keywords, str):
            _, keywords = _extract_tags("," + keywords, ",")
        elif isinstance(keywords, int):
            keywords = [str(keywords)]
        all_keywords = [str(key) for key in keywords]
        all_keywords = all_keywords + _extract_tags(description, "#")[1]
        old_keywords = all_keywords
        all_keywords = sorted(set(all_keywords + _extract_tags(description, "#")[1]))
    # Force use str
    return all_keywords, old_keywords


def tag_images_for_google_drive(
        input_files: AbstractSet[Path],
        database: Optional[Path],
        extra_tags: Optional[Set[str]],
        tag_file: Optional[Path] = None,
        from_files: bool = False,
        from_db: bool = False,
        force: bool = False,
        dry: bool = False,
        verbose: int = 0) -> Tuple[Mapping[Path, Tuple[str, Sequence[str]]], Mapping[Path, Tuple[str, Sequence[str]]]]:
    """
    Analyse csv and files to extract tag and inject hash tag in description.
    :param database: The CSV file or None
    :param input_files: A set of filename
    :param tag_file: A filename to save all tags or None
    :param from_file: A boolean value to use only the files names
    :param from_db: A boolean value to use only the CSV file
    :param dry: True to simulate the modification in files.
    :return: A tuple with the new data base and the description of all modified files.
    """
    assert bool(from_files) + bool(from_db) < 2
    merge = not from_db and not from_files
    assert not ((from_db or merge) and not database)

    if not extra_tags:
        extra_tags = set()

    updated_files: Dict[Path, Tuple[str, List[str]]] = {}  # Files to update

    update_descriptions = False
    ref_descriptions: Dict[Path, Tuple[str, List[str]]] = {}
    description_date = 0.0

    if database and database.is_file():
        description_date = database.stat().st_mtime
        with open(str(database), 'rt', encoding='utf-8') as csv_file:
            rows = csv.reader(csv_file, delimiter=',')
            ref_descriptions = {Path(row[0]): _extract_tags(row[1], '#') for row in rows if len(row) == 2}
    else:
        update_descriptions = True
    if not shutil.which("exiftool"):
        LOGGER.error("Install exiftool in PATH before to use tag_images_for_google_drive")
        raise OSError(-1, "exiftool not found")

    with ExifTool() as exif_tool:
        # 1. Update images files
        update_descriptions = _manage_files(exif_tool,
                                            input_files,
                                            from_db,
                                            from_files,
                                            ref_descriptions,
                                            extra_tags,
                                            update_descriptions,
                                            updated_files,
                                            force,
                                            verbose)

        # 2. Apply the descriptions file
        update_descriptions = _manage_db(exif_tool,
                                         description_date,
                                         from_db,
                                         from_files,
                                         merge,
                                         ref_descriptions,
                                         extra_tags,
                                         update_descriptions,
                                         updated_files,
                                         force,
                                         verbose)

        # 3. Apply update files
        _manage_updated_files(exif_tool, dry, updated_files)

        # 4. Update description
        _manage_updated_db(database, dry, ref_descriptions, update_descriptions)

    # 5. Count tags
    all_tags: AbstractSet[str] = set()
    nb_files = len(ref_descriptions)
    nb_total_tags = 0
    for _, (_, keywords) in ref_descriptions.items():
        nb_total_tags += len(keywords)
        all_tags = set(all_tags).union(keywords)
    LOGGER.info(f"Use {nb_total_tags} tags in {nb_files} files, with a dictionary of {len(all_tags)} "
                f"({int(nb_files / nb_total_tags * 100) if nb_total_tags else 0} t/f).")
    _manage_tags_file(all_tags, dry, tag_file)

    LOGGER.debug("Done")
    return ref_descriptions, updated_files


def _manage_tags_file(all_tags, dry, tag_file):
    if not dry and tag_file:
        all_tags = sorted(set(all_tags))
        old_version = tag_file.with_suffix(".txt.old")
        try:
            if tag_file.exists():
                shutil.copy(tag_file, old_version)
            with open(str(tag_file), 'w', encoding="utf-8") as f:
                f.seek(0)
                f.truncate()
                for tag in all_tags:
                    f.write(tag + "\n")
            old_version.unlink()
        finally:
            if old_version.is_file():
                if tag_file.exists():
                    tag_file.unlink()
                if old_version.exists():
                    shutil.copy(old_version, tag_file)
                    old_version.unlink()


def _manage_files(exif_tool: ExifTool,
                  input_files: AbstractSet[Path],
                  from_db: bool,
                  from_files: bool,
                  ref_descriptions: Dict[Path, Tuple[str, List[str]]],
                  extratags: Set[str],
                  update_descriptions: bool,
                  updated_files: Dict[Path, Tuple[str, List[str]]],
                  force: bool,
                  verbose: int = 0) -> bool:
    LOGGER.debug("Update images...")
    for file in input_files:
        file = file.absolute()
        rel_file = file.relative_to(Path.cwd())
        if verbose >= 3:
            LOGGER.debug(f"Inspect {rel_file}...")
        must_update, description, keywords = _extract_description_and_tags(exif_tool, file)
        target_keywords = keywords
        db_keywords: List[str] = []
        if rel_file in ref_descriptions:
            (_, db_keywords) = ref_descriptions[rel_file]
            target_keywords += db_keywords
        if from_db and rel_file in ref_descriptions:
            target_keywords = db_keywords
        if from_files:
            target_keywords = keywords
        if from_files and rel_file in ref_descriptions and ref_descriptions[rel_file] != description:
            LOGGER.debug(f"{'Update' if rel_file in ref_descriptions else 'Add'} in csv file '{rel_file}'")
            update_descriptions = True
            ref_descriptions[rel_file] = (description, keywords)
        if force:
            must_update = True
        if not set(extratags).issubset(target_keywords):
            must_update = True
            target_keywords.extend(extratags)
        if must_update:
            update_descriptions = True
            updated_files[file] = (description, target_keywords)
        if must_update or rel_file not in ref_descriptions:
            LOGGER.debug(f"{'Update' if rel_file in ref_descriptions else 'Add'} in csv file '{rel_file}'")
            update_descriptions = True
            ref_descriptions[rel_file] = (description, target_keywords)
    LOGGER.debug("Update images done")
    return update_descriptions


def _manage_db(exif_tool: ExifTool,  # pylint: disable=too-many-arguments,too-many-branches
               description_date: float,
               from_db: bool,
               from_files: bool,
               merge: bool,
               ref_descriptions: Dict[Path, Tuple[str, List[str]]],
               extratags: Set[str],
               update_descriptions: bool,
               updated_files: Dict[Path, Tuple[str, List[str]]],
               force: bool,
               verbose: int = 0) -> bool:
    if not from_files:
        LOGGER.debug("Apply csv file...")
        remove_files = []
        for rel_file, (desc, tags) in ref_descriptions.items():
            if verbose >= 3:
                LOGGER.debug(f"Inspect {rel_file}...")
            file = rel_file.absolute()
            if file.is_file():
                try:
                    file_date = file.stat().st_mtime
                    must_update, description, keywords = _extract_description_and_tags(exif_tool, file)
                    if not keywords:
                        LOGGER.warning(f"{file.relative_to(Path.cwd())} has not tags")
                    if not from_files and force:
                        must_update = True
                    if not from_files and not set(extratags).issubset(keywords):
                        tags = sorted(tags)
                    if must_update:
                        updated_files[file] = (description, keywords)
                    if from_db and (must_update or desc != description or tags != keywords):
                        LOGGER.debug(f"Refresh file '{file}'")
                        updated_files[file] = (desc, tags)
                    elif (must_update or desc != description or tags != keywords):
                        update_descriptions = _manage_file_and_db(desc, description, description_date, file, file_date,
                                                                  from_db, keywords, merge, ref_descriptions, rel_file,
                                                                  tags, update_descriptions, updated_files)
                except JSONDecodeError:
                    LOGGER.warning(f"Impossible to analyse '{file}' (JSONDecodeError)")
            else:
                # LOGGER.debug(f"Remove in csv file '{rel_file}'")
                remove_files.append(rel_file)

        for rel_file in remove_files:
            ref_descriptions.pop(rel_file)
        LOGGER.debug("Apply csv file done")
    return update_descriptions


def _manage_updated_files(exif_tools: ExifTool,
                          dry: bool,
                          updated_files: Dict[Path, Tuple[str, List[str]]]) -> None:
    LOGGER.debug("Update identified files in csv ...")
    for file, (description, keywords) in updated_files.items():
        str_tags = "#" + " #".join(keywords) if len(keywords) > 0 else ""
        description = description.strip()
        description_and_tags = f"{description} {str_tags}" if len(description) > 0 else str_tags
        if description_and_tags != "":
            LOGGER.info(f"Update '{file.relative_to(Path.cwd())}' with '{description_and_tags}'")
            if not dry:
                subject = SEP.join(keywords)
                iptc_keywords = subject
                while len(iptc_keywords) >= 63:
                    iptc_keywords = iptc_keywords[:iptc_keywords.rfind(',')]
                _set_tags(exif_tools,
                          {"Comment": description_and_tags,
                           "Description": description_and_tags,
                           "ImageDescription": description,
                           "Caption-Abstract": description,
                           "Headline": description,
                           "KeyWords": iptc_keywords,
                           "Subject": subject,
                           "HierarchicalSubject": subject,
                           },
                          file)


def _manage_updated_db(database: Optional[Path],
                       dry: bool,
                       ref_descriptions: Dict[Path, Tuple[str, List[str]]],
                       update_descriptions: bool):
    if database and not dry and update_descriptions:
        try:
            LOGGER.debug("Update csv file...")
            # Update "in place"
            old_version = database.with_suffix(".csv.old")
            if database.exists():
                shutil.copy(database, old_version)
            with open(str(database), 'wt', encoding='utf-8', newline='\n') as f:
                f.seek(0)
                f.truncate()
                writer = csv.writer(f)
                ref_descriptions = {key: ref_descriptions[key] for key in sorted(ref_descriptions.keys())}
                for path, (description, keywords) in ref_descriptions.items():
                    str_tags = "#" + " #".join(keywords) if len(keywords) > 0 else ""
                    description = description.strip()
                    description_and_tags = f"{description} {str_tags}" if len(description) > 0 else str_tags
                    if str(path):
                        writer.writerow([path.as_posix(), description_and_tags])
                # Commit change
                f.close()
                if old_version.is_file():
                    old_version.unlink()
        finally:
            if old_version.is_file():
                if old_version.exists():
                    if database.exists():
                        database.unlink()
                    shutil.copy(old_version, database)
                    old_version.unlink()


def _manage_file_and_db(desc: str,  # pylint: disable=R0913
                        description: str,
                        description_date: float,
                        file: Path,
                        file_date: float,
                        from_db: bool,
                        keywords: List[str],
                        merge: bool,
                        ref_descriptions: Dict[Path, Tuple[str, List[str]]],
                        rel_file: Path,
                        tags: List[str],
                        update_descriptions: bool,
                        updated_files: Dict[Path, Tuple[str, List[str]]]) -> bool:
    if from_db:
        updated_files[file] = (desc, tags)
    else:
        if merge:
            new_tags = sorted(set(tags).union(keywords))
            if new_tags != keywords:
                updated_files[file] = (desc, new_tags)
            if new_tags != tags:
                tags = new_tags
                update_descriptions = True
                ref_descriptions[rel_file] = (desc, tags)
                LOGGER.debug(
                    f"{'Update' if rel_file in ref_descriptions else 'Add'} "
                    f"in csv file '{rel_file}'")

            # Use recent description
            if desc == "":
                desc = description
            if file_date > description_date and desc != "":
                desc = description
                update_descriptions = True
                ref_descriptions[rel_file] = (desc, new_tags)
                updated_files[file] = (desc, new_tags)
                LOGGER.debug(
                    f"{'Update' if rel_file in ref_descriptions else 'Add'} "
                    f"in csv file '{rel_file}'")

        if desc == "" or tags != keywords:
            update_descriptions = True
            if desc == "":
                desc = description
            LOGGER.debug(
                f"{'Update' if rel_file in ref_descriptions else 'Add'} "
                f"in csv file '{rel_file}'")
            ref_descriptions[rel_file] = (desc, tags)
            updated_files[file] = (desc, new_tags)
        LOGGER.debug(f"Refresh file '{file}' with {tags}")
        updated_files[file] = (desc, tags)
    return update_descriptions


@click.command(short_help="Synchronize and update csv and files hash-tags")
@click.argument("input_files", metavar='<selected files>', type=Glob(default_suffix="**/*.jpg", recursive=True),
                nargs=-1)
@click.option("--db", metavar='<csv file>', type=click_pathlib.Path(exists=False, file_okay=True), help="CSV database")
@click.option("--tagfile", metavar='<tag file>', type=click_pathlib.Path(exists=False, file_okay=True), default=None,
              help="Export all tags in text file")
@click.option("--tag", "-t", multiple=True, help="Add extra tag")
@click.option("-f", '--from-files', is_flag=True, default=False, help="Use only tags from files")
@click.option("-fdb", '--from-db', is_flag=True, default=False, help="Use only tags from csv file")
@click.option("--dry", default=False, is_flag=True, help="Dry run")
@click.option("-v", '--verbose', count=True, help="Verbosity")
@click.option("--force", is_flag=True, help="Force to update all images files")
def main(  # pylint: disable=C0103
        input_files: Sequence[Sequence[Path]],
        db: Optional[Path] = None,
        tagfile: Optional[Path] = None,
        tag: Optional[Sequence[str]] = None,
        from_files: bool = False,
        from_db: bool = False,
        dry: bool = False,
        force: bool = False,
        verbose: int = 0) -> int:
    """Synchronize CSV database and PNG/JPEG files to add #hashtag in image description.
       Then, you can synchronize all files with Google drive.

       Google drive use only the description meta-data to index an image.
       After this synchronisation it's possible to search an image with
       "type:image an_hash_tag".

       By default, this tools merge the tags from CSV and files.
    """
    try:
        level_mapping = [logging.WARN, logging.INFO, logging.DEBUG]

        init_logger(LOGGER, level_mapping[min(verbose, len(level_mapping) - 1)])

        if not db:
            from_files = True

        if bool(from_files) + bool(from_db) > 1:
            LOGGER.error("--from_files/-f and --from_db/-fdb are mutually incompatible")
            return -1
        if (from_db or not from_files) and not db:
            LOGGER.error("Set --db <file> with --from_files or --merge")
            return -1

        if not db and not input_files:
            ctx = click.get_current_context()
            click.echo(ctx.get_help())
            return 0

        # Flat map input files
        all_input_files = set(itertools.chain(*input_files))
        ref_descriptions, _ = tag_images_for_google_drive(
            input_files=all_input_files,
            database=db,
            from_files=from_files,
            from_db=from_db,
            extra_tags=set(tag if tag else []),
            tag_file=tagfile,
            force=force,
            dry=dry,
            verbose=verbose)
        if verbose >= 3:
            LOGGER.debug("File csv file:")
            for path, (description, tags) in ref_descriptions.items():
                LOGGER.debug(f"{path}, {description} {tags}")
        return 0
    except OSError as e:
        return e.errno


if __name__ == '__main__':
    if sys.platform.startswith("win"):
        from ctypes import windll

        windll.kernel32.SetConsoleCP(65001)  # Force Code Page console à UTF-8
    sys.exit(main(standalone_mode=False))  # pylint: disable=E1120,E1123
