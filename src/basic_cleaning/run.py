#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    # Download input artifact
    logger.info(f'Downloading artifact from {args.input_artifact}')
    local_path = wandb.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)

    # Drop outliers
    logger.info(f'Dropping price outliers( min:{args.min_price}, max:{args.max_price}')
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    logger.info(f'Converting last_review to datetime')
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Save as CSV
    logger.info(f'Saving the cleaned data')
    df.to_csv("clean_sample.csv", index=False)

    # Upload the artifact to wandb
    logger.info(f'Uploading the data as {args.output_artifact}')
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of input artifact.",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of output artifact.",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of output artifact.",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of output artifact.",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum value of price.",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum value of price.",
        required=True
    )


    args = parser.parse_args()

    go(args)
