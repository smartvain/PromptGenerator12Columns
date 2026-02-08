import random

class PromptGeneratorNSFWAction:
    DEBUG = True

    NSFW_ACTIONS = """completely naked
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
standing carry
against wall
lifted during sex
anal sex
oral sex
deepthroat
facefuck
blowjob
giving handjob
titfuck
paizuri
breast squeeze
squirting
female ejaculation
intense orgasm
ahegao orgasm
rolling eyes orgasm
tongue out orgasm
heart-shaped pupils
creampie
cum inside pussy
cum overflow
cum on body
cum on face
cum in mouth
bukkake
cum covered
cum dripping from pussy
after sex
post-orgasm bliss
bound wrists
bound ankles
shibari
rope bondage
collar and leash
wearing collar
wearing blindfold
wearing nipple clamps
wearing anal plug
wearing tail plug
fox tail plug
cat tail plug
vibrator inside
remote vibrator
public masturbation
public sex
glory hole
gangbang
tentacle sex
monster sex
lactating
milking breasts
fisting pussy
x-ray view
internal cumshot
breeding
begging for sex
masturbating
scissoring
tribadism
69 position
facesitting
eating pussy
licking anus
anilingus
footjob
thighjob
sweaty sex
oiled body
covered in oil
covered in sweat
covered in cum
body writing
free use
mind break
broken mind orgasm
mind broken
empty eyes
drooling
trembling orgasm
shaking from pleasure
pussy juice trail
wet pussy
dripping wet
aroused swollen clit
pulsating pussy
extreme ahegao
tongue fully out
tears of pleasure
blushing intensely
heart eyes
completely submissive
completely dominant
ecstatic expression
pleasure overload"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "NSFW_Action": ("STRING", {"multiline": True, "default": cls.NSFW_ACTIONS}),
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

    def _pick_one(self, text_block):
        if not text_block:
            return ""
        lines = [l.strip() for l in str(text_block).splitlines()
                 if l.strip() and not l.strip().startswith('#')]
        return random.choice(lines) if lines else ""

    def generate(self, **kwargs):
        seed = random.randint(0, 0xffffffffffffffff)
        random.seed(seed)

        prompt_text = kwargs.get("prompt", "").strip()
        nsfw_action = self._pick_one(kwargs.get("NSFW_Action", ""))

        sep = ", " if kwargs.get("use_commas", True) else "\n"

        parts = []
        if prompt_text:
            parts.append(prompt_text)
        if nsfw_action:
            parts.append(nsfw_action)

        result = sep.join(parts)

        if self.DEBUG:
            print(f"\n[NSFW Action Generator] Seed: {seed}\n→ {result}\n{'─' * 80}")

        return (result,)

NODE_CLASS_MAPPINGS = {
    "PromptGeneratorNSFWAction": PromptGeneratorNSFWAction
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptGeneratorNSFWAction": "NSFW Action Prompt Generator"
}
