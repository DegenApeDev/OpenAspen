import click
import asyncio
import json
from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config, LLMConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


@click.group()
@click.version_option(version="0.1.0")
def main() -> None:
    pass


@main.command()
@click.option("--name", default="my_tree", help="Name of the tree project")
@click.option("--output", default="tree.json", help="Output file path")
def init(name: str, output: str) -> None:
    template = {
        "name": name,
        "branches": [
            {
                "name": "general_assistant",
                "description": "General purpose assistant for various tasks",
                "llm_provider": "openai",
                "system_prompt": "You are a helpful AI assistant.",
            }
        ],
        "llm_providers": {
            "openai": {
                "provider": "openai",
                "model": "gpt-4-turbo-preview",
            }
        },
    }

    Path(output).write_text(json.dumps(template, indent=2))
    click.echo(f"✅ Initialized OpenAspen tree: {output}")
    click.echo(f"📝 Edit {output} to customize your tree")
    click.echo(f"🚀 Run with: openaspen run {output}")


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--query", "-q", help="Query to execute")
@click.option("--interactive", "-i", is_flag=True, help="Interactive mode")
def run(config_file: str, query: str, interactive: bool) -> None:
    asyncio.run(_run_async(config_file, query, interactive))


async def _run_async(config_file: str, query: str, interactive: bool) -> None:
    config_data = json.loads(Path(config_file).read_text())

    llm_configs = {}
    for name, config in config_data.get("llm_providers", {}).items():
        llm_configs[name] = create_llm_config(**config)

    tree = OpenAspenTree.from_dict(config_data, llm_configs)

    click.echo(tree.visualize())
    click.echo()

    if interactive:
        click.echo("🌲 OpenAspen Interactive Mode (type 'exit' to quit)")
        while True:
            user_query = click.prompt("Query", type=str)
            if user_query.lower() in ["exit", "quit"]:
                break

            result = await tree.execute(user_query)
            click.echo(json.dumps(result, indent=2))
            click.echo()
    elif query:
        result = await tree.execute(query)
        click.echo(json.dumps(result, indent=2))
    else:
        click.echo("❌ Provide --query or use --interactive mode")


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
def visualize(config_file: str) -> None:
    config_data = json.loads(Path(config_file).read_text())

    llm_configs = {}
    for name, config in config_data.get("llm_providers", {}).items():
        llm_configs[name] = create_llm_config(**config)

    tree = OpenAspenTree.from_dict(config_data, llm_configs)
    click.echo(tree.visualize())


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
def info(config_file: str) -> None:
    config_data = json.loads(Path(config_file).read_text())

    click.echo(f"🌲 Tree: {config_data.get('name', 'Unnamed')}")
    click.echo(f"🌿 Branches: {len(config_data.get('branches', []))}")
    click.echo(f"🤖 LLM Providers: {', '.join(config_data.get('llm_providers', {}).keys())}")

    for branch in config_data.get("branches", []):
        click.echo(f"\n  Branch: {branch['name']}")
        click.echo(f"    Description: {branch.get('description', 'N/A')}")
        click.echo(f"    LLM: {branch.get('llm_provider', 'default')}")


if __name__ == "__main__":
    main()
