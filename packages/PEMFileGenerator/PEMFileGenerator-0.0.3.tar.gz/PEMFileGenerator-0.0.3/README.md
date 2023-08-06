## PEM File Generator

Basically this library will help user to generate SSH PEM file for access remote server and disable password login to
remote server. But If user want to keep password login option enable.It can be also available

## Example

```python
"""
Generate SSH PEM File Example
"""
from PEMFileGenerator.ssh_pem import Generate

# Password login disable
gen = Generate(ip="192.168.56.15", user="vagrant", password="vagrant")
try:
    gen.run()
except Exception as err:
    print(err)

# Password login enable
gen1 = Generate(ip="192.168.56.15", user="vagrant", password="vagrant", password_auth_disable=False)
try:
    gen1.run()
except Exception as err:
    print(err)

```

To learn more [Documentation](https://github.com/vubon/PEMFileGenerator/blob/main/docs/GUIDE.md).

## Changelog

See [Changelog](CHANGELOG.md)

## License

MIT
