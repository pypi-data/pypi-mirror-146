config_h = configure_file(
    output: 'config.h',
    configuration: conf
)

private_incdir = include_directories('.')

config_dep = declare_dependency(
  include_directories : private_incdir,
  sources: config_h)
