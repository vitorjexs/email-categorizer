import React, { useState } from "react";
import "./app.css";

export default function App() {
  const [texto, setTexto] = useState("");
  const [arquivo, setArquivo] = useState(null);
  const [categoria, setCategoria] = useState("");
  const [resposta, setResposta] = useState("");
  const [resultados, setResultados] = useState([]);

  function handleArquivo(e) {
    const file = e.target.files[0];
    if (!file) return;
    if (!["application/pdf", "text/plain"].includes(file.type)) {
      alert("Apenas arquivos .txt ou .pdf são permitidos.");
      return;
    }
    setArquivo(file);
  }

  async function handleEnviar() {
    if (!texto && !arquivo) {
      alert("Insira um texto ou selecione um arquivo.");
      return;
    }

    const formData = new FormData();

    if (texto) formData.append("texto", texto);
    if (arquivo) formData.append("arquivo", arquivo);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/classificar-e-responder",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        alert(`Erro: ${errorData.error || "Erro desconhecido"}`);
        return;
      }

      const data = await response.json();

      setResultados((valor) => [
        ...valor,
        { categoria: data.categorizacao, resposta: data.sugestaoDeResposta },
      ]);

      setCategoria(data.categorizacao);
      setResposta(data.sugestaoDeResposta);
    } catch (error) {
      console.error("Erro ao enviar:", error);
      alert("Erro de rede ou servidor fora do ar.");
    }
  }
  function renderizarResultados() {
    return resultados.map((item, index) => (
      <div key={index} style={{ marginTop: 30 }}>
        <h2>Resultado #{index + 1}</h2>
        <p>
          <strong>Categoria:</strong> {item.categoria}
        </p>
        <p>
          <strong>Resposta Sugerida:</strong>
        </p>
        <blockquote style={{ background: "#f0f0f0", padding: 10 }}>
          {item.resposta}
        </blockquote>
      </div>
    ));
  }

  return (
    <div className="app-container">
      <h1>Classificador de E-mails</h1>

      <form className="formulario">
        <label htmlFor="upload-arquivo" className="botao-enviar">
          Escolher arquivo
        </label>
        <input
          id="upload-arquivo"
          type="file"
          accept=".txt,.pdf"
          onChange={handleArquivo}
          style={{ display: "none" }}
        />

        <label>Ou insira o texto do e-mail:</label>

        <textarea
          className="textarea-input"
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          placeholder="Cole aqui o conteúdo do e-mail..."
        />

        <button className="botao-enviar" onClick={handleEnviar}>
          Enviar para Processamento
        </button>
      </form>
      <div className="secao-resultados">{renderizarResultados()}</div>
    </div>
  );
}
