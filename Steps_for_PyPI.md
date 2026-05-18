# Step-by-Step Upload to PyPI

Now that your files are ready, run these exact commands in your terminal:

**Step 1**: Install the build tools**
```bash
pip install build twine
```

**Step 2**: Create the "Distribution Artifacts"
This command bundles your code into a .whl (Wheel) and a .tar.gz file
```sh
python -m build
```

You will now see a new folder called `/dist` in your project.

**Step 3**: Upload to PyPI
```sh
python -m twine upload dist/*
```

**Step 4**: Provide Credentials
Username: Type __token__
Password: Paste your PyPI API Token (the one starting with pypi-...)


# What happens next?
Once this is done, anyone in the world (including you on a different computer) can run:

1. `pip install mcp-people-finder`
2. `people-finder`

**And that's it!** You have officially published a library.

**Wait, what about Docker?**
You only need Docker if you want to host this code yourself as a "Live URL" for an agent to call over the internet. Since you've published it to PyPI, your "Production-Grade" strategy is now: "Distribute via PyPI, Deploy via Cloud Run."