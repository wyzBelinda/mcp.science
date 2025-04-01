import asyncio
import argparse

from .server import serve


def main():
    parser = argparse.ArgumentParser("a general python code execution tool")

    parser.add_argument(
        "--code",
        type=str,
        help="code to execute"
    )
    args = parser.parse_args()

    asyncio.run(serve(args.code))

if __name__ == "__main__":
    main()
