#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# This script preprocesses the sparse feature files (binary npy) to such that
# the IDs become contiguous (with frequency thresholding applied).
# The results are saved in new binary (npy) files.

import argparse
import os
import sys
from typing import List

from torchrec.datasets.criteo import BinaryCriteoUtils


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Criteo sparse -> contiguous preprocessing script. "
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        required=True,
        help="Input directory containing the sparse features in numpy format (.npy). Files in the directory "
        "should be named day_{0-23}_sparse.npy.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Output directory to store npy files.",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    """
    This function processes the sparse features (.npy) to be contiguous
    and saves the result in a separate (.npy) file.

    Args:
        argv (List[str]): Command line args.

    Returns:
        None.
    """

    args = parse_args(argv)
    input_dir = args.input_dir
    output_dir = args.output_dir

    # Look for files that end in "_sparse.npy" since this processing is
    # only applied to sparse data.
    input_files = list(
        map(
            lambda f: os.path.join(input_dir, f),
            list(filter(lambda f: f.endswith("_sparse.npy"), os.listdir(input_dir))),
        )
    )
    if not input_files:
        raise ValueError(
            f"There are no files that end with '_sparse.npy' in this directory: {input_dir}"
        )

    print(f"Processing files in: {input_files}. Outputs will be saved to {output_dir}.")
    BinaryCriteoUtils.sparse_to_contiguous(input_files, output_dir)
    print("Done processing.")


if __name__ == "__main__":
    main(sys.argv[1:])
