from importlib.metadata import entry_points
import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
   name='liste-iniziativa-medica',
   version='0.0.8',
   description='Package per il generatore di liste di Iniziativa Medica',
   license="MIT",
   long_description=long_description,
   author='Nicolò Nalin',
   author_email='niconalin@gmail.com',
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'pandas>=1.4.2',
        'pdfkit>=1.0.0',
        'PyPDF2>=1.27.3',
        'reportlab>=3.6.9',
    ],
    entry_points= {
        'console_scripts': [
            'liste-iniziativa-medica=src.gui:run'
        ]
    }
)