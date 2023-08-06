def perimetro_area (lados = []):
    a = lados[0];
    b = lados[1];
    c = lados[2];

    if a + b > c and a + c > b and b + c > a:
        # TODO Preencha a formula do perímeto do triangulo (soma de todos os lados).
        perimetro = a + b + c
        return f"Perimetro = {perimetro:.1f}"
    else:
        # TODO Preencha a formula da área do trapézio: AREA = ((A + B) x C) / 2
        area = ((a + b) * c) / 2
        return f"Area = {area:.1f}"