import os
import json
from transformers import AutoTokenizer, AutoModel
import re

# Caminhos para os arquivos JSON
biographies = './data/complete_artists_biographies_translated.json'
albums = './data/complete_artists_albums.json'
songs = './data/complete_artists_songs.json'

names_bio = [b['Name'] for b in biographies]
names_songs = [s['Name'] for s in songs]
names_albums = [a['Name'] for a in albums]

# Função para consolidar os dados dos três arquivos em um único campo de conteúdo
def consolidate_artist_data(biographies, albums, songs):
    consolidated_data = []

    for bio in biographies:
        artist_name = bio['Name']

        # Pegar a biografia
        biography_content = bio['Biography'].get('Content', '')

        # Encontrar álbuns do artista (se houver)
        artist_albums = next((a['Albums'] for a in albums if a['Name'] == artist_name), [])
        albums_text = '\n'.join([f"{album['title']} ({album['year']})" for album in artist_albums]) if artist_albums else "Nenhum álbum disponível"

        # Encontrar músicas do artista (se houver)
        artist_songs = next((s['Songs'] for s in songs if s['Name'] == artist_name), [])
        songs_text = ', '.join(artist_songs) if artist_songs else "Nenhuma música disponível"

        # Criar o conteúdo consolidado
        content = f"Biografia: {biography_content}\n\nÁlbuns: {albums_text}\n\nMúsicas: {songs_text}"

        # Adicionar ao array de dados consolidados
        consolidated_data.append({
            "artist": artist_name,
            "content": content
        })

    return consolidated_data


all_data = consolidate_artist_data(biographies, albums, songs)
contents = []

for bio in all_data:
    contents.append(bio["content"])

contents_ = '\n\n'.join(contents)

contents_ = re.sub(r'\n{3,}', '\n\n', contents_)