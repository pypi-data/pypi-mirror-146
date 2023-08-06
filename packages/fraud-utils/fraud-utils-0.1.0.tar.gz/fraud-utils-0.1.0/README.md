This is a tool for publishing dummy packages to the external PyPi with the same name as our internal packages. 
Reason for it: if we fail to do `pip install` from our internal PyPi it will install from public and prevent us from installing malicious packages.

For a new version

```
bash publish.sh fraud-utils 0.1.5 ilmarine y
```
Arguments:
1) New package name
2) New version
3) Old package name (existing folder name in the repository)
4) Upload to prod pypi (y/n) - do we need to upload only to the test pypi or to live as well
The first argument is a new package name, the second - a new version, the third - old package name (existing folder name in the repository),


It will upload package to the test public pypi https://test.pypi.org/legacy/ and to live if requested https://pypi.org/legacy/.

Credentials can be found in 1password (Model Lifecycle space).