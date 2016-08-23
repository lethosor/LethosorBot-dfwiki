import core
core.run(
    generator=core.site.Pages['Template:New in v0.42'].embeddedin(namespace='DF2014', filterredir='nonredirects'),
    old_pattern='{{creaturedesc}}\n{{new in v0.42}}',
    new_pattern='{{new in v0.42}}\n{{creaturedesc}}',
    summary='Fixing template order: {{new in v0.42}} before {{creaturedesc}}',
)
