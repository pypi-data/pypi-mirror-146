import setuptools

setuptools.setup(
	name='bgRemoverApp',
	version='1.18',
	author='kos94ok',
	author_email='mirmen999@mail.ru',
	description='Background Remover App',
	url='https://github.com/kos94ok/bgRemoverApp',
	packages = ['bgRemoverApp'],
    package_data={
        'bgRemoverApp': ['tracer/*', 'u2net/*'],
    },
	classifiers=[
		"Programming Language :: Python :: 3.9",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.9',
)