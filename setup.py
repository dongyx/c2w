import setuptools

from src.c2w.c2w import __version__ as version

with open('README.md', 'r') as fp:
	longdesc = fp.read()

setuptools.setup(
	name='c2w',
	version=version,
	author='DONG Yuxuan',
	author_email='dong_yuxuan@icloud.com',
	description='convert CLI programs to web services',
	long_description=longdesc,
	long_description_content_type='text/markdown',
	url='https://github.com/dongyx/c2w',
	license='MIT',
	python_requires='>=3.6',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
	],

	packages=setuptools.find_packages('src'),
	package_dir={ '': 'src' },

	entry_points={
		'console_scripts': [
			'c2w=c2w.c2w:main'
		]
	}
)
