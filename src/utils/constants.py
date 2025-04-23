IMAGE_CATEGORY = {
    "Graph": [
        'a picture including curve graph',
        'a picture including linear graph',
        'a picture including bar graph',
    ],

    "Formula": [
        'equilibrium expression for a chemical',
        'formula including fraction or symbols',
    ],
    "Text": [
        'a formula including Korean',
        'a sentence including Hangul',
        'a photo including Hangul',
        'a sentence including English',
    ]
}

FORMULA_OCR_MESSAGE = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "Extract mathematical expressions in LaTeX format"}
        ]
    },
]