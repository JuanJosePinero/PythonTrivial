# Preguntas y respuestas para un trivial en Python

preguntas = [
    {
        "pregunta": "¿Quién rompió la raspberry?",
        "opciones": ["a) Iván y Josema.", "b) El rubio de Javi.", "c) Nadie.", "d) Todos menos Iván y Josema."],
        "respuesta_correcta": "a"
    },
    {
        "pregunta": "¿Quién es el mejor profesor?",
        "opciones": ["a) Félix", "b) Raúl Gil", "c) Raúl Reyes", "d) Rafa"],
        "respuesta_correcta": "b"
    },
    {
        "pregunta": "¿Félix corrige muy estricto?",
        "opciones": ["a) Sí", "b) Sí, solo un poco.", "c) No, corrige bien.", "d) No, es culpa nuestra por no saber hacerlo."],
        "respuesta_correcta": "d"
    },
    {
        "pregunta": "¿A alguien le gusta los buenos días?",
        "opciones": ["a) Sí, a todos.", "b) No, ¿a quién le gusta eso?", "c) Sí, solo al director y a Raúl Reyes.", "d) Ninguna respuesta es correcta."],
        "respuesta_correcta": "b"
    },
    {
        "pregunta": "¿Qué castigo se le asignó a Josema y a Iván?",
        "opciones": ["a) Limpiar la clase.", "b) Actuar en el Belén Navideño.", "c) Dar los buenos días.", "d) Comprar churros para la clase."],
        "respuesta_correcta": "b"
    }
]

# Guardar las preguntas en un archivo o base de datos si es necesario
# Aquí las imprimimos como ejemplo
for idx, pregunta in enumerate(preguntas, start=1):
    print(f"Pregunta {idx}: {pregunta['pregunta']}")
    for opcion in pregunta['opciones']:
        print(opcion)
    print(f"Respuesta correcta: {pregunta['respuesta_correcta']}")
