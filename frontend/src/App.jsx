import React, { useState } from 'react';

function App() {
  const [inputText, setInputText] = useState('');
  const [correctedText, setCorrectedText] = useState('');

  const handleChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSpellCheck = async () => {
    try {
      const response = await fetch('http://localhost:7000/spellcheck', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
        throw new Error('서버 오류 발생');
      }

      const data = await response.json();
      setCorrectedText(data.corrected_text);
    } catch (error) {
      setCorrectedText('오류가 발생했습니다.');
    }
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial' }}>
      <h1>맞춤법 교정기</h1>
      <textarea
        value={inputText}
        onChange={handleChange}
        rows="5"
        cols="50"
        placeholder="텍스트를 입력하세요"
      />
      <br />
      <button onClick={handleSpellCheck}>교정하기</button>
      <h3>교정 결과:</h3>
      <p>{correctedText}</p>
    </div>
  );
}

export default App;
