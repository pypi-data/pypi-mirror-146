import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ciclops",
    version="0.0.1",
    author="Elysia Chou, Hanrui Zhang, Yuanfang Guan",
    author_email="elysian@umich.edu, rayezh@umich.edu, gyuanfan@umich.edu",
    description="Pipeline for building clinical outcome prediction models on training dataset and transfer learning on validation datasets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GuanLab/Predict-Malaria-ART-Resistance",
    project_urls={
        "Bug Tracker": "https://github.com/GuanLab/Predict-Malaria-ART-Resistance/issues",
    },
    keywords=['Bioinformatics','Transfer Learning','Machine Learning','Transcriptomics','Research', 'Clinical Outcome Prediction'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where = 'src'),
    entry_points = {
        'console_scripts': [
            'ciclops = ciclops.__main__:main'
            ]
        },
    python_requires=">=3.8",
    install_requires = [
        'numpy >=1.21.5',
        'pandas >=1.4.1',
        'matplotlib >=3.5.1',
        'matplotlib-venn >=0.11.7',
        'scikit-learn >=1.0.2',
        'scipy >=1.8.0',
        'lightgbm >=3.3.2',
        'shap >=0.35.0',
        'xgboost >=1.5.2',
        'tqdm >=4.63.0'
    ]
)
