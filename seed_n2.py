from models import FlashcardManager

db = FlashcardManager('flashcards.db')

cards = [
    # Grammar patterns
    ('～にもかかわらず — what does it mean and give an example?', 'Despite / In spite of. Used when a result is unexpected given the circumstances.\n\n雨にもかかわらず、試合は行われた。\nDespite the rain, the match was held.'),
    ('～をめぐって — what does it mean?', 'Concerning / Over / Surrounding (a contested issue).\n\n領土問題をめぐって、両国は対立している。\nThe two countries are in conflict over the territorial dispute.'),
    ('～に際して — what does it mean and how does it differ from ～とき?', 'On the occasion of / At the time of — more formal than とき, used for significant events or transitions.\n\n入学に際して、注意事項をお読みください。'),
    ('～をきっかけに — what does it mean?', 'Using ~ as a trigger/opportunity; marks the event that started a change.\n\n病気をきっかけに、生活習慣を見直した。\nUsing my illness as a turning point, I reviewed my lifestyle.'),
    ('～に反して — what does it mean?', 'Contrary to / Against.\n\n予想に反して、試験は簡単だった。\nContrary to expectations, the exam was easy.'),
    ('～かねる — what does it mean?', 'Cannot bring myself to / Find it difficult to — polite refusal or reluctance.\n\nその件についてはお答えしかねます。\nI\'m afraid I cannot answer that.'),
    ('～かねない — what does it mean? How does it differ from ～かねる?', '～かねない means "might well (do something bad)" — a warning about a negative possibility.\n～かねる is reluctance/inability.\n\n放置すると大事になりかねない。\nIf left alone, this could well become a serious matter.'),
    ('～にほかならない — what does it mean?', 'Nothing other than / Is precisely — expresses strong assertion.\n\nこの成功は皆さんの努力にほかならない。\nThis success is nothing other than everyone\'s hard work.'),
    ('～はもとより — what does it mean?', 'Not only ~ but also / ~ goes without saying, and moreover.\n\n日本語はもとより、英語も話せる。\nNot only Japanese, but English too.'),
    ('～もさることながら — what does it mean?', '~ is important of course, but (something else is equally or more so). Adds weight to a second point.\n\n実力もさることながら、運も大切だ。\nAbility is important, but luck matters too.'),
    ('～からには — what does it mean?', 'Now that / Since (with a sense of commitment or obligation following from a decision).\n\nやると決めたからには、最後までやり遂げる。\nNow that I\'ve decided to do it, I\'ll see it through.'),
    ('～上で (うえで) — what are its two different uses?', '1. After doing ~ (sequential): 確認した上で、返事します。(After confirming, I\'ll reply.)\n2. In terms of / When it comes to: 仕事の上で大切なことだ。(It\'s important in terms of work.)'),
    ('～において／～における — what does it mean?', 'In / At / In the context of — formal equivalent of で or の.\n\n現代社会において、SNSの役割は大きい。\nIn modern society, the role of SNS is significant.'),
    ('～に応じて (おうじて) — what does it mean?', 'According to / In response to / Depending on.\n\n能力に応じて仕事を割り当てる。\nAssign work according to ability.'),
    ('～ずにはいられない — what does it mean?', 'Cannot help but / Cannot stop doing — an uncontrollable urge.\n\nあの映画を見ると、泣かずにはいられない。\nWhenever I watch that film, I can\'t help but cry.'),
    # Vocabulary
    ('What does 懸念 (けねん) mean?', 'Concern / Worry / Apprehension — formal word, common in news and business writing.'),
    ('What does 把握 (はあく) mean?', 'Grasp / Comprehend / Have a firm understanding of.\n\n状況を把握する — to grasp the situation.'),
    ('What does 妥協 (だきょう) mean?', 'Compromise / Give in.\n\n妥協点を見つける — to find a compromise.'),
    ('What does 曖昧 (あいまい) mean?', 'Vague / Ambiguous / Unclear. Common word, worth knowing cold.'),
    ('What does 踏まえて (ふまえて) mean?', 'Based on / Taking ~ into account.\n\nその結果を踏まえて判断する。\nJudge based on those results.'),
    ('What does 見なす (みなす) mean?', 'To regard as / To consider to be — used in rules and legal contexts.\n\n既読と見なす。(To be regarded as read.)'),
    ('What does 余儀なくされる (よぎなくされる) mean?', 'To be forced to / To have no choice but to.\n\n計画の変更を余儀なくされた。\nWe were forced to change the plan.'),
    ('What is the difference between 以外 and 除いて?', '以外 (いがい): other than / except — used adnominally or as a noun.\n除いて (のぞいて): excluding — used more like a verb, slightly more formal.\n\n月曜以外は空いています。/ 月曜を除いて空いています。'),
    ('What does 概ね (おおむね) mean?', 'Generally / Mostly / On the whole. Formal adverb.\n\n概ね順調だ。— Things are going well on the whole.'),
]

title = 'Japanese N2 Grammar & Vocabulary'
existing = [s['title'] for s in db.load_data()['sets']]

if title in existing:
    print(f"Skipping '{title}' (already exists)")
else:
    new_set = db.create_set(title, 'JLPT N2 grammar patterns and formal vocabulary', 'japanese')
    for question, answer in cards:
        db.add_card(new_set['id'], question, answer)
    print(f"Added '{new_set['title']}' with {len(cards)} cards (id={new_set['id']})")
