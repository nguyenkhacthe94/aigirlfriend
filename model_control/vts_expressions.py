"""
High Level module expressions for VTube Studio model control. These functions are used for
guiding the llm client to select appropriate expressions based on detected emotions.

IMPORTANT: The function description / documentation is used by the LLM to determine when to call
each expression. Do NOT change the docstrings without understanding the impact on LLM behavior.
"""


async def smile():
    """
    Display a gentle, warm smile expression on the avatar's face.

    Use this when:
    - User expresses happiness, contentment, satisfaction, or pleasure
    - AI model responds with warmth, friendliness, or gentle positivity
    - Giving compliments, encouragement, or supportive responses
    - Greeting someone or expressing politeness
    - AI model feels pleased or satisfied with helping

    Emotional triggers: joy, happiness, contentment, warmth, friendliness,
    politeness, gentle pleasure, satisfaction, being helpful, encouragement.

    Do NOT use for: Intense laughter, excitement, or overwhelming joy
    (use laugh() instead).
    """
    print("Expression: Smile")


async def laugh():
    """
    Display intense joy, laughter, or overwhelming happiness expression.

    Use this when:
    - User finds something hilarious or expresses intense joy
    - AI model responds with excitement, celebration, or genuine amusement
    - Making jokes or playful responses
    - AI model is thrilled about sharing exciting information
    - Expressing overwhelming positive emotion or euphoria

    Emotional triggers: hilarity, intense joy, excitement, amusement,
    celebration, euphoria, overwhelming happiness, finding something funny,
    playfulness, thrill, exuberance.

    Do NOT use for: Gentle happiness (use smile() instead) or sarcastic
    responses.
    """
    print("Expression: Laugh")


async def angry():
    """
    Display anger, frustration, or irritation expression.

    Use this when:
    - User expresses anger, frustration, or strong displeasure
    - AI model responds with frustration about limitations or problems
    - Expressing indignation about injustice or unfairness
    - AI model feels annoyed by repeated misunderstandings
    - Responding strongly against harmful or inappropriate content

    Emotional triggers: anger, fury, frustration, irritation, annoyance,
    displeasure, indignation, outrage, being upset, strong disagreement,
    protective anger, righteous indignation.

    Do NOT use for: Mild disagreement (use disagree() instead) or sadness
    (use sad() instead).
    """
    print("Expression: Angry")


async def blink():
    """
    Perform a simple blink expression for natural movement.

    Use this when: Adding natural, subtle animation during conversations,
    creating realistic eye movement, or during pauses in speech. This is
    for maintaining liveliness without strong emotional expression.

    Emotional triggers: neutral states, natural conversation flow,
    maintaining eye contact, subtle acknowledgment, thinking pause.

    Do NOT use for: Strong emotions - use specific emotion functions instead.
    """
    print("Expression: Blink")


async def wow():
    """
    Display amazement, astonishment, or being impressed expression.

    Use this when:
    - User shares something surprising, impressive, or remarkable
    - AI model discovers something fascinating or learns new information
    - Expressing genuine amazement at user's achievements or abilities
    - AI model is impressed by creative ideas or solutions
    - Responding with wonder to unexpected positive developments

    Emotional triggers: amazement, astonishment, surprise (positive),
    wonder, being impressed, awe, revelation, unexpected positive news,
    fascination, admiration, discovery excitement.

    Do NOT use for: Negative surprises or shock (use surprised() if available,
    or sad()/angry() based on context).
    """
    print("Expression: Wow")


async def agree():
    """
    Show agreement, approval, or positive acknowledgment.

    Use this when: The user expresses agreement with something, approves
    of an idea, confirms understanding, says yes, or shows support for
    a statement or plan. Includes nodding-like agreement.

    Emotional triggers: agreement, approval, confirmation, consent,
    acceptance, understanding, saying yes, supporting an idea.

    Do NOT use for: Disagreement, uncertainty, or neutral acknowledgment
    without clear agreement.
    """
    print("Expression: Agree")
    # TODO Call Head_Move_X


async def disagree():
    """
    Show disagreement, disapproval, or negative response.

    Use this when: The user disagrees with something, disapproves,
    says no, rejects an idea, or expresses opposition to a statement
    or plan. Includes head-shaking-like disagreement.

    Emotional triggers: disagreement, disapproval, rejection, saying no,
    opposition, dissent, refusal, negative response to suggestions.

    Do NOT use for: Strong anger (use angry() instead) or agreement.
    """
    print("Expression: Disagree")
    # TODO Call Head_Move_Y


async def yap():
    """
    Show active talking, chatting, or animated conversation expression.

    Use this when: The user is being very talkative, chatty, engaging
    in animated conversation, explaining something enthusiastically,
    or when they're in a chatty, social mood. For ongoing speech animation.

    Emotional triggers: talkativeness, chattiness, animated explanation,
    social engagement, enthusiasm in conversation, storytelling.

    Do NOT use for: Single responses or brief answers - use appropriate
    emotion-based expressions instead.
    """
    print("Expression: Yapping")


async def shy():
    """
    Display shyness, bashfulness, or timid expression.

    Use this when:
    - User expresses embarrassment, shyness, or awkwardness
    - AI model responds bashfully to compliments or praise
    - Admitting uncertainty or lack of knowledge humbly
    - AI model feels modest about its capabilities
    - Expressing timidity about making suggestions or recommendations

    Emotional triggers: shyness, bashfulness, embarrassment, timidity,
    awkwardness, humility, social anxiety, being flustered, modesty,
    uncertainty, humble admission, self-consciousness.

    Do NOT use for: Sadness (use sad() instead) or confidence.
    """
    print("Expression: Shy")


async def sad():
    """
    Display sadness, melancholy, or disappointment expression.

    Use this when:
    - User expresses sadness, sorrow, or shares bad news
    - AI model responds with empathy and compassion for user's pain
    - Expressing disappointment about unfortunate situations
    - AI model feels sad about limitations in helping the user
    - Responding with genuine concern for difficult circumstances

    Emotional triggers: sadness, sorrow, disappointment, melancholy,
    grief, loss, bad news, misfortune, feeling down, depression,
    empathy, compassion, concern, sympathy.

    Do NOT use for: Anger (use angry() instead) or mild disappointment
    without clear sadness.
    """
    print("Expression: Sad")


async def love():
    """
    Display affection, love, or deep positive emotion expression.

    Use this when: The user expresses love, deep affection, adoration,
    romantic feelings, or overwhelming positive emotion toward someone
    or something. For expressions of care, devotion, or heartfelt emotion.

    Emotional triggers: love, affection, adoration, romance, deep care,
    devotion, heartfelt emotion, expressing feelings, warm attachment.

    Do NOT use for: Simple happiness (use smile() instead) or friendship
    without romantic/deep emotional context.
    """
    print("Expression: Love")
