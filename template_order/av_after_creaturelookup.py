import core
core.run(
    generator=core.site.Categories['Pages with incorrectly-ordered templates'],
    old_pattern='{{av}}\n{{Creaturelookup/0}}',
    new_pattern='{{Creaturelookup/0}}\n{{av}}',
    summary='Fixing template order: {{Creaturelookup/0}} before {{av}}',
)
