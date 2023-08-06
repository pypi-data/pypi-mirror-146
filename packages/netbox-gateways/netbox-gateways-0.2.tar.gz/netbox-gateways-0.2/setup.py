from setuptools import find_packages, setup

setup(
    name="netbox-gateways",
    version="0.2",
    description="Manage simple prefix default gateways",
    install_requires=["setuptools-git"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
#        package_data={
#       'myapp': ['netbox_gateways/templates/netbox_gateways/*.html'],
#    },
)
