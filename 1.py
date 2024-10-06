import argparse
import asyncio
import logging

logger = logging.getLogger(__name__)


from aiopath import AsyncPath
from aioshutil import copyfile


async def read_folder(path: AsyncPath, output: AsyncPath) -> None:
    try:
        async for item in path.iterdir():
            if await item.is_dir():
                logger.info(f"Reading folder: {item}")
                await read_folder(item, output)
            else:
                await copy_file(item, output)
    except Exception as e:
        logger.warning(f"Reading error: {e}")


async def copy_file(file: AsyncPath, output: AsyncPath) -> None:
    extension_name = file.suffix[1:]
    extension_folder = output / extension_name
    try:
        await extension_folder.mkdir(exist_ok=True, parents=True)
        logger.info(f"Creating folder: {extension_folder}")
    except Exception as e:
        logger.warning(f"Error creating folder: {e}")

    try:
        await copyfile(file, extension_folder / file.name)
        logger.info(f"Copying file: {file}")
    except Exception as e:
        logger.warning(f"Error copying file: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
    logger.info("Started")

    parser = argparse.ArgumentParser()

    parser.add_argument("source", type=AsyncPath)
    parser.add_argument("output", type=AsyncPath, nargs="?", default=AsyncPath("dist"))

    args = parser.parse_args()

    source = args.source
    output = args.output

    asyncio.run(read_folder(source, output))
    logger.info("Finished")
