from setuptools import setup

setup(name='audit_pkg',
      version='1.4.1',
      description='Package auditors distributions',
      packages=['audit_pkg'],
      author_email='fgantua32@gmail.com',
     
      package_data={  # Optional
        "audit_pkg": ["src/*"],
      },
      entry_points={  # Optional
        "console_scripts": [
            "audit-pkg=audit_pkg.main:start",
        ],
      },
      zip_safe=False)