# captif-cpx


## Development

### Pre-commit hooks

Install pre-commit hooks `pre-commit install`.

The pre-commit hooks will run before each commit. To bypass the pre-commit hooks use `git commit -m 'message' --no-verify`.

### Testing

Run `./coverage.sh`.

### Publish to PyPI

Pushing a tag with format `v*` to the remote repository will trigger a publish to PyPI:

```bash
git fetch . dev:master                # merge dev with master
git tag -a v0.1 -m "initial release"  # add a version tag
git push origin master v0.1           # push master and tag
```

A Github workflow will automatically run the tests and publish to PyPI if all tests pass.
