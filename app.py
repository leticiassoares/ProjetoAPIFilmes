import streamlit as st
import json
import requests
import os

api_key = "3082ff680e18b05a2c788ba9ff0df1da"
api_url = "https://api.themoviedb.org/3/search/multi"
fav_path = "favoritos.json"

def main():
    st.title("🎬 - Seja bem-vindo ao ProjetoAPIFilmes")
    st.write("Aqui você pode encontar filmes e séries.")
    aba = st.sidebar.selectbox("Escolha uma opção:", ["Buscar", "Favoritos"])


    def carregar_fav():
        if os.path.exists(fav_path):
            with open(fav_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return[]

    def salvar_fav(favoritos):
        with open(fav_path, "w", encoding="utf-8") as f:
            json.dump(favoritos, f, ensure_ascii=False, indent=4)

    def buscar_titulos(query):
        params = {
            "api_key": api_key,
            "query": query,
            "language": "pt-BR"
        }
        resp = requests.get(api_url, params=params)
        return resp.json().get("results", [])


    if aba == "Buscar":
        busca = st.text_input("Digite o nome do filme ou série: ")
        if busca:
            resultados = buscar_titulos(busca)
            for item in resultados:
                titulo = item.get("title") or item.get("name")
                descricao = item.get("overview", "Não encontrei descrição para esse filme/série.")
                imagem = item.get("poster_path")
                url_img = f"https://image.tmdb.org/t/p/w200{imagem}" if imagem else None
                st.subheader(titulo)
                if url_img:
                    st.image(url_img, width=150)
                st.write(descricao)
                if st.button(f"💖 - Adicionar aos favoritos", key=titulo):
                    favoritos = carregar_fav()
                    if titulo not in favoritos:
                        favoritos.append(titulo)
                        salvar_fav(favoritos)
                        st.success(f"{titulo} foi adicionado aos favoritos.")

    elif aba == "Favoritos":
        st.header("Meus favoritos:")
        favoritos = carregar_fav()
        if not favoritos:
            st.write("Nenhum favorito salvo.")
        for fav in favoritos:
            st.write(f"• {fav}")

if __name__ == "__main__":
    main()