def buscar_clima():
    cidade = entrada_cidade.get()
    if not cidade:
        messagebox.showwarning("Aviso", "Digite uma cidade.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"

    try:
        resposta = requests.get(url)
        dados = resposta.json()

        if resposta.status_code != 200:
            raise Exception(dados.get("message", "Erro ao buscar dados"))

        temp = dados["main"]["temp"]
        sensacao = dados["main"]["feels_like"]
        clima = dados["weather"][0]["description"]

        # Criar dataframe e gerar gráfico
        df = pd.DataFrame({
            "Tipo": ["Temperatura", "Sensação Térmica"],
            "Valor (°C)": [temp, sensacao]
        })

        plt.figure(figsize=(6, 4))
        plt.bar(df["Tipo"], df["Valor (°C)"], color=["blue", "orange"])
        plt.title(f"Clima em {cidade.title()}: {clima}")
        plt.ylabel("Temperatura (°C)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Erro", str(e)) 