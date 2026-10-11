# Jack & Lucy image library

Character images for worksheets (Nano Banana Pro, flat vector style, plain white background, 2048×2048).
`characters.json` has the same list in machine-readable form.

**Dialogue rule:** Lucy images marked `right` face the right side, Jack images marked `left` face the left side,
so in a chat-style dialogue Lucy sits on the left and Jack on the right, looking at each other.

| # | Who | Pose | Facing | Best for |
|---|-----|------|--------|----------|
| 01 | Lucy | thumbs-up | front | Tip box, encouragement |
| 02 | Jack | lightbulb-idea | front | Quick tip, grammar corner |
| 03 | Lucy | did-you-know | front | Fun fact box |
| 04 | Jack | thinking | front | Quiz / think about it |
| 05 | Lucy | writing | front | Writing task, your turn |
| 06 | Jack | listening | front | Listening exercise |
| 07 | Lucy | great-job | front | Score, answer key, well done |
| 08 | Jack | waving | front | Share with us, goodbye |
| 09 | Lucy | talking-right | right | Dialogue – Lucy speaking |
| 10 | Lucy | listening-right | right | Dialogue – Lucy listening |
| 11 | Lucy | asking-right | right | Dialogue – Lucy asking |
| 12 | Lucy | laughing-right | right | Dialogue – Lucy laughing |
| 13 | Jack | talking-left | left | Dialogue – Jack speaking |
| 14 | Jack | listening-left | left | Dialogue – Jack listening |
| 15 | Jack | shrug-left | left | Dialogue – Jack answering, 'who knows?' |
| 16 | Jack | surprised-left | left | Dialogue – Jack surprised |
| 17 | Lucy | winter-tea | front | Winter, cold weather, hot drinks |
| 18 | Jack | winter-cold | front | Winter, cold weather |
| 19 | Lucy | glasses-book | front | Reading, studying |
| 20 | Jack | glasses-laptop | front | Technology, online, work |
| 21 | Jack | eating-sandwich | front | Food, eating, lunch |
| 22 | Lucy | eating-apple | front | Healthy food, snacks |
| 23 | Jack | hot-chocolate | front | Cosy, comfort, winter drinks |
| 24 | Lucy | summer-hat | front | Summer, sun, holidays |
| 25 | Jack | rain-umbrella | front | Rain, weather |
| 26 | Jack | sleepy-morning | front | Sleep, mornings, tiredness |
| 27 | Lucy | morning-stretch | front | Morning routine, energy, exercise |
| 28 | Lucy | travel | front | Travel, airports, holidays |
| 29 | Duo | high-five | front | Answer key, celebration |
| 30 | Duo | waving | front | Cover, goodbye, end page |
| 31 | Duo | quiz | front | Quiz section, questions |
| 32 | Lucy | coffee-chat-right | right | Dialogue – Lucy chatting with a coffee (café scenes) |
| 33 | Jack | blue-scarf-good-morning | front | Greetings, mornings, winter, bus stop |
| 34 | Lucy | shy-but-brave | front | Shyness, confidence, first tries |
| 35 | Jack | reading-card | front | Kindness, messages, emotional stories |

**Tip:** when making new images, attach one of these library images as the reference so the flat style stays the same.

## Using an image on a coloured background
`python3 cutout.py <image.jpg> <out.png> [--keep x,y ...]` removes the white background.
Large white gaps enclosed by the character (between hair and arms) are removed too; small white
details (eye whites, highlights) stay. Use `--keep x,y` for large white parts that must stay
(teeth, big eyes, paper, whipped cream…).
Always check the result on a dark background before using it.
