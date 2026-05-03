from models import FlashcardManager

db = FlashcardManager('flashcards.db')

existing = [s['title'] for s in db.load_data()['sets']]

sets = [
    {
        'title': 'Japanese Essentials',
        'description': 'Core vocabulary, particles, and grammar patterns',
        'category': 'japanese',
        'cards': [
            ('What does ありがとう (arigatou) mean?', 'Thank you'),
            ('What does すみません (sumimasen) mean?', 'Excuse me / Sorry — used to get attention or apologise'),
            ('Translate: 私は学生です (watashi wa gakusei desu)', 'I am a student'),
            ('What is the particle は (wa) used for?', 'Topic marker — marks what the sentence is about'),
            ('What is the particle を (wo/o) used for?', 'Object marker — marks the direct object of a verb'),
            ('What is the particle に (ni) used for?', 'Direction, location of existence, or point in time'),
            ('What is the particle が (ga) used for?', 'Subject marker — often used for emphasis or new information'),
            ('How do you say "Where is the station?" in Japanese?', '駅はどこですか？ (eki wa doko desu ka?)'),
            ('What does ～ている (te iru) express?', 'Ongoing action or current state — equivalent to "-ing"'),
            ('Conjugate 食べる (taberu, to eat) into past tense', '食べた (tabeta)'),
            ('What does もう mean in "もう食べた"?', 'Already — "I already ate"'),
            ('What is the difference between 行きます and 行った?', '行きます is present/future polite; 行った is plain past'),
            ('How do you count flat objects (paper, sheets) in Japanese?', '一枚、二枚、三枚 (ichimai, nimai, sanmai) — use 枚 (mai)'),
            ('What does ～たい express?', 'Want to do something — attach to verb stem: 食べたい = want to eat'),
            ('What does でも mean at the start of a sentence?', 'But / However'),
        ],
    },
    {
        'title': 'TypeScript',
        'description': 'Types, generics, and patterns worth knowing cold',
        'category': 'programming',
        'cards': [
            ('What is the difference between `type` and `interface` in TypeScript?', '`interface` is extendable via `extends` and declaration merging; `type` can express unions, intersections, and mapped types. Prefer `interface` for object shapes, `type` for everything else.'),
            ('What does the `unknown` type enforce compared to `any`?', '`unknown` requires a type check before use; `any` skips all checks. Use `unknown` for values whose type you genuinely don\'t know.'),
            ('What is a union type? Give an example.', 'A value that can be one of several types.\n\ntype Status = "active" | "inactive" | "pending"'),
            ('What is a type guard?', 'A runtime check that narrows a type within a block.\n\nif (typeof x === "string") { /* x is string here */ }'),
            ('What does `keyof` do?', 'Produces a union of the keys of a type.\n\ntype K = keyof { a: number; b: string } // "a" | "b"'),
            ('What does `Partial<T>` do?', 'Makes all properties of T optional.'),
            ('What does `Required<T>` do?', 'Makes all properties of T required — opposite of Partial.'),
            ('What does `Pick<T, K>` do?', 'Creates a type with only the specified keys from T.\n\nPick<User, "id" | "name">'),
            ('What does `Omit<T, K>` do?', 'Creates a type with all keys of T except the specified ones.'),
            ('What is a generic constraint? Give an example.', 'Limits what types a generic accepts.\n\nfunction getLength<T extends { length: number }>(x: T): number'),
            ('What is the `as const` assertion used for?', 'Infers the narrowest possible literal types and makes the value readonly.\n\nconst config = { env: "prod" } as const // env: "prod", not string'),
            ('What is the `never` type?', 'A type with no values — used for exhaustive checks or functions that never return (throw or infinite loop).'),
            ('What is a discriminated union?', 'A union of types that share a common literal field used to distinguish them.\n\ntype Shape = { kind: "circle"; radius: number } | { kind: "rect"; width: number }'),
            ('What does the `infer` keyword do inside a conditional type?', 'Captures a type variable within a conditional type.\n\ntype ReturnType<T> = T extends (...args: any[]) => infer R ? R : never'),
        ],
    },
    {
        'title': 'Python',
        'description': 'Language features, idioms, and stdlib worth knowing',
        'category': 'programming',
        'cards': [
            ('What does a list comprehension look like? Give an example.', '[expression for item in iterable if condition]\n\nsquares = [x**2 for x in range(10) if x % 2 == 0]'),
            ('What is a generator function and how does it differ from a regular function?', 'Uses `yield` instead of `return`. Returns a generator object that produces values lazily — only computes each value when asked.'),
            ('What does `*args` capture in a function signature?', 'All positional arguments beyond those explicitly named, as a tuple.'),
            ('What does `**kwargs` capture?', 'All keyword arguments not explicitly named, as a dict.'),
            ('What is a decorator?', 'A function that wraps another function to extend its behaviour without modifying it.\n\n@timer\ndef my_func(): ...'),
            ('What does `@contextmanager` from `contextlib` let you do?', 'Write a generator-based context manager without a full class. yield once; code before yield is __enter__, after is __exit__.'),
            ('What is the difference between `is` and `==`?', '`==` checks value equality; `is` checks identity (same object in memory). Never use `is` to compare values like strings or numbers.'),
            ('What does `enumerate()` do?', 'Wraps an iterable and yields (index, value) tuples.\n\nfor i, val in enumerate(items):'),
            ('What does `zip()` do?', 'Pairs up elements from multiple iterables into tuples, stopping at the shortest.\n\nfor a, b in zip(list1, list2):'),
            ('What is the difference between a shallow copy and a deep copy?', 'Shallow copy duplicates the container but not nested objects (copy.copy). Deep copy duplicates everything recursively (copy.deepcopy).'),
            ('What does `__dunder__` mean?', 'Double-underscore methods (magic/dunder methods) define how objects behave with built-in operations — e.g. __len__, __str__, __eq__.'),
            ('What does `dict.get(key, default)` do differently from `dict[key]`?', 'Returns the default instead of raising KeyError when the key is missing.'),
            ('What is a set and when would you use one?', 'An unordered collection of unique values. Use it for membership tests, deduplication, and set operations (union, intersection).'),
            ('What does `if __name__ == "__main__":` do?', 'Runs the block only when the file is executed directly, not when it\'s imported as a module.'),
        ],
    },
    {
        'title': 'Software Engineering',
        'description': 'Principles, patterns, and concepts that come up everywhere',
        'category': 'programming',
        'cards': [
            ('What does SOLID stand for?', 'Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion'),
            ('What is the Single Responsibility Principle?', 'A class or module should have one reason to change — one job.'),
            ('What is the Open/Closed Principle?', 'Open for extension, closed for modification — add behaviour by extending, not by editing existing code.'),
            ('What is the Liskov Substitution Principle?', 'A subclass should be usable wherever its parent is used without breaking correctness.'),
            ('What is Dependency Injection?', 'Passing dependencies into a component rather than constructing them inside it. Makes code testable and decoupled.'),
            ('What is the difference between coupling and cohesion?', 'Coupling: how much modules depend on each other (low is good). Cohesion: how related the responsibilities within a module are (high is good).'),
            ('What is idempotency?', 'An operation is idempotent if applying it multiple times has the same effect as applying it once. GET and PUT are idempotent; POST is not.'),
            ('What is the difference between SQL and NoSQL databases?', 'SQL: relational, fixed schema, ACID transactions. NoSQL: flexible schema, various data models (document, key-value, graph), trades some consistency for scale.'),
            ('What does ACID stand for in databases?', 'Atomicity, Consistency, Isolation, Durability — properties that guarantee reliable transactions.'),
            ('What is an index in a database and what is the trade-off?', 'A data structure that speeds up reads on a column. Trade-off: slower writes and more storage.'),
            ('What is the difference between a stack and a queue?', 'Stack: LIFO (last in, first out). Queue: FIFO (first in, first out).'),
            ('What is Big O notation used for?', 'Describing how runtime or space requirements grow as input size grows — independent of hardware.'),
            ('What is O(n log n) and which sorting algorithms achieve it?', 'Better than O(n²), worse than O(n). Merge sort and heap sort always achieve it; quicksort achieves it on average.'),
            ('What is a race condition?', 'When the outcome depends on the timing or ordering of concurrent operations — a bug that only appears under specific scheduling.'),
            ('What is the difference between concurrency and parallelism?', 'Concurrency: multiple tasks in progress at once (may interleave on one core). Parallelism: multiple tasks literally executing simultaneously on multiple cores.'),
        ],
    },
    {
        'title': 'Debugging',
        'description': 'Strategies, tools, and mental models for finding what\'s broken',
        'category': 'programming',
        'cards': [
            ('What is the first thing to do when facing an unfamiliar bug?', 'Reproduce it reliably. A bug you can\'t reproduce consistently is nearly impossible to fix.'),
            ('What is a minimal reproducible example (MRE)?', 'The smallest amount of code that still triggers the bug. Stripping irrelevant code clarifies the cause and makes it easy to share.'),
            ('What is rubber duck debugging?', 'Explaining your code line-by-line to an inanimate object. The act of articulating the problem often reveals the flaw.'),
            ('What is a stack trace and what does it tell you?', 'The call chain at the moment an error occurred — read it bottom-up to find where your code caused the problem.'),
            ('What is the difference between a syntax error and a runtime error?', 'Syntax error: code won\'t parse (caught before running). Runtime error: code is valid but fails during execution.'),
            ('What is a breakpoint?', 'A marker that pauses execution at a specific line so you can inspect state in a debugger.'),
            ('What does "bisecting" mean in debugging?', 'Narrowing down a bug by splitting the search space in half — like git bisect, which finds which commit introduced a regression.'),
            ('What does `git bisect` do?', 'Binary searches your commit history to find the first commit that introduced a bug. Mark commits good/bad until it isolates the culprit.'),
            ('What is an off-by-one error?', 'A bug where a loop or index is out by one — common causes: using < vs <=, 0-based vs 1-based indexing.'),
            ('What is a null pointer / NoneType error and how do you avoid it?', 'Accessing a property or calling a method on a null/None value. Avoid by checking for None before use or using optional chaining.'),
            ('What is the difference between logging and print debugging?', 'Print debugging is quick but left in code or removed manually. Logging is structured, levelled (DEBUG/INFO/ERROR), and can be toggled without code changes.'),
            ('What does it mean for a test to be "flaky"?', 'It passes sometimes and fails other times without code changes — usually caused by timing, shared state, or external dependencies.'),
            ('What is a regression?', 'A bug in behaviour that previously worked — introduced by a code change. Caught by running the full test suite after every change.'),
        ],
    },
]

total_cards = 0
for s in sets:
    if s['title'] in existing:
        print(f"  Skipping '{s['title']}' (already exists)")
        continue
    new_set = db.create_set(s['title'], s['description'], s['category'])
    for question, answer in s['cards']:
        db.add_card(new_set['id'], question, answer)
    total_cards += len(s['cards'])
    print(f"  {s['title']} - {len(s['cards'])} cards")

print(f"\n{len(sets)} sets, {total_cards} cards total")
