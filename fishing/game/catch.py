"""
catch: hook-vs-fish catch detection.
"""


def check_catch(hook, fish_list):
    """
    Return the first fish whose hitbox overlaps the hook, or None.
    """
    hook_rect = hook.get_rect()
    for fish in fish_list:
        if hook_rect.colliderect(fish.get_rect()):
            return fish
    return None
