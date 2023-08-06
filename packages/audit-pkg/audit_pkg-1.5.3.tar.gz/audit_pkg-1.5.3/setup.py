from setuptools import setup 



setup(
      name='audit_pkg',
      version='1.5.3',
      description='Package auditors distributions',
      packages=['audit_pkg'],
      
   
      package_data={  # Optional
        "audit_pkg": ["dist/main","dist/main.exe"],
      },
      entry_points={  # Optional
        "console_scripts": [
            "audit-pkg=audit_pkg.__main__:main",
        ],
      },
      zip_safe=False
    )