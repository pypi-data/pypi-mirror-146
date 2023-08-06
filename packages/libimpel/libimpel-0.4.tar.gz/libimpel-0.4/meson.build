project('libimpel', 'c',
  version : '0.4',
  default_options : ['warning_level=2'])

incdir = include_directories(['.', 'src'])

conf = configuration_data()
cc = meson.get_compiler('c')

subdir('private')
subdir('src')
subdir('libimpel')
