import subprocess
from pathlib import Path

import click
from click import Command


def train_run() -> Command:
    @click.command(
        context_settings={"ignore_unknown_options": True},
        name="train",
        short_help="Train a model",
    )
    @click.option(
        "-f",
        "--file",
        help="File used for training",
        type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
        default="tools/train.py",
    )
    @click.option(
        "--running_mode",
        help="The running mode used for training",
        type=str,
        default="debug",
    )
    @click.option(
        "--config",
        help="File used for training",
        type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    )
    def run(file: click.Path, running_mode: str, config: click.Path) -> None:
        """
        Execute a new run on Spell with a Bendai configuration file
        """
        click.echo("⚙️ Running training...")
        command = ["poetry", "run", "python", file, "--running_mode", running_mode]
        if config is not None:
            command.extend(["--config", config])
        subprocess.run(command)

    return run


def test_run() -> Command:
    @click.command(
        context_settings={"ignore_unknown_options": True},
        name="test",
        short_help="Test a model given a checkpoint",
    )
    @click.option(
        "-f",
        "--file",
        help="File used for testing",
        type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
        default="tools/test.py",
    )
    @click.option(
        "--running_mode",
        help="The running mode used for testing",
        type=str,
        default="debug",
    )
    @click.option(
        "--config",
        help="File used for testing",
        type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    )
    def run(file: click.Path, running_mode: str, config: click.Path) -> None:
        """
        Execute a new run on Spell with a Bendai configuration file
        """
        click.echo("⚙️ Running testing...")
        command = ["poetry", "run", "python", file, "--running_mode", running_mode]
        if config is not None:
            command.extend(["--config", config])
        subprocess.run(command)

    return run


def predict_run() -> Command:
    @click.command(
        context_settings={"ignore_unknown_options": True},
        name="predict",
        short_help="Test a model given a checkpoint",
    )
    @click.option(
        "-f",
        "--file",
        help="File used for prediction",
        type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
        default="tools/predict.py",
    )
    @click.option(
        "--running_mode",
        help="The running mode used for prediction",
        type=str,
        default="debug",
    )
    @click.option(
        "--config",
        help="File used for prediction",
        type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    )
    def run(file: click.Path, running_mode: str, config: click.Path) -> None:
        """
        Execute a new run on Spell with a Bendai configuration file
        """
        click.echo("⚙️ Running prediction...")
        command = ["poetry", "run", "python", file, "--running_mode", running_mode]
        if config is not None:
            command.extend(["--config", config])
        subprocess.run(command)

    return run


if __name__ == "__main__":

    run = train_run()
    run()
