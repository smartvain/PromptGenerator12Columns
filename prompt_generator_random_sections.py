import random
import re

class PromptGeneratorRandomSections:
    DEBUG = True

    DEFAULT_SECTIONS = """[NSFW Action]
completely naked
fully nude
spreading legs wide
spreading pussy
fingering herself
fingering pussy
riding cowgirl position
reverse cowgirl
doggy style
bent over
presenting ass
ass up face down
on all fours
kneeling
missionary position
legs behind head
full nelson
mating press
prone bone
spooning sex
standing sex
against wall
lifted during sex
oral sex
deepthroat
blowjob
titfuck
paizuri
breast squeeze
squirting
intense orgasm
ahegao orgasm
rolling eyes orgasm
tongue out orgasm
creampie
cum inside pussy
cum on body
cum on face
after sex
post-orgasm bliss
bound wrists
shibari
rope bondage
collar and leash
vibrator inside
masturbating
69 position
facesitting
sweaty sex
oiled body
trembling orgasm
shaking from pleasure
wet pussy
dripping wet
extreme ahegao
tears of pleasure
completely submissive
completely dominant
pleasure overload

[Expression]
ahegao tongue out
blushing intensely
lustful bedroom eyes
shy biting lip
seductive smirk
orgasm face
rolling eyes back
desperate needy look
ecstatic open mouth
heart pupils
moaning expression
eyes half closed
face twisted in pleasure
face of pure lust
face of total submission"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "random_sections": ("STRING", {"multiline": True, "default": cls.DEFAULT_SECTIONS}),
            },
            "optional": {
                "use_commas": ("BOOLEAN", {"default": True, "label_on": "Use Commas", "label_off": "New Lines"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "generate"
    CATEGORY = "Random Prompt Generators"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return random.random()

    def _split_merged_items(self, text):
        """Split text that may contain multiple items joined by 3+ spaces."""
        items = re.split(r'\s{3,}', text)
        return [item.strip() for item in items if item.strip() and not item.strip().startswith('#')]

    def _parse_sections(self, text):
        sections = []
        current_name = None
        current_lines = []

        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            match = re.match(r'^\[(.+?)\](.*)', stripped)
            if match:
                if current_name is not None and current_lines:
                    sections.append((current_name, current_lines))
                current_name = match.group(1).strip()
                current_lines = []
                remaining = match.group(2).strip()
                if remaining:
                    current_lines.extend(self._split_merged_items(remaining))
            elif current_name is not None:
                current_lines.extend(self._split_merged_items(stripped))

        if current_name is not None and current_lines:
            sections.append((current_name, current_lines))

        return sections

    def generate(self, **kwargs):
        seed = random.randint(0, 0xffffffffffffffff)
        random.seed(seed)

        prompt_text = kwargs.get("prompt", "").strip()
        sections_text = kwargs.get("random_sections", "")
        use_commas = kwargs.get("use_commas", True)

        sections = self._parse_sections(sections_text)

        sep = ", " if use_commas else "\n"
        parts = []

        if prompt_text:
            parts.append(prompt_text)

        for name, lines in sections:
            pinned = [l[1:] for l in lines if l.startswith('$')]
            candidates = [l for l in lines if not l.startswith('$') and not l.startswith('!')]
            if pinned:
                pick = pinned[0]
            elif candidates:
                pick = random.choice(candidates)
            else:
                continue
            parts.append(pick)

        result = sep.join(parts)

        if self.DEBUG:
            picks = []
            idx = 1 if prompt_text else 0
            for name, lines in sections:
                excluded = [l[1:] for l in lines if l.startswith('!')]
                has_pinned = any(l.startswith('$') for l in lines)
                candidates = [l for l in lines if not l.startswith('$') and not l.startswith('!')]
                if has_pinned or candidates:
                    if idx < len(parts):
                        mark = " (pinned)" if has_pinned else ""
                        excluded_str = f" | excluded: {', '.join(excluded)}" if excluded else ""
                        picks.append(f"  [{name}] → {parts[idx]}{mark}{excluded_str}")
                        idx += 1
                else:
                    picks.append(f"  [{name}] → (all excluded, skipped)")
            picks_str = "\n".join(picks)
            print(f"\n[Random Sections Generator] Seed: {seed}\n{picks_str}\n→ {result}\n{'─' * 80}")

        return (result,)

NODE_CLASS_MAPPINGS = {
    "PromptGeneratorRandomSections": PromptGeneratorRandomSections
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptGeneratorRandomSections": "Random Sections Prompt Generator"
}
