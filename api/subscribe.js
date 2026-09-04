// api/subscribe.js — Vercel Serverless Function
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', 'https://steelframing.com.br');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const email = (req.body?.EMAIL || req.body?.email || '').trim();
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'E-mail inválido' });
  }

  const apiKey = process.env.BREVO_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'API key não configurada' });

  try {
    const r = await fetch('https://api.brevo.com/v3/contacts', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'content-type': 'application/json',
        'api-key': apiKey,
      },
      body: JSON.stringify({
        email,
        listIds: [3],
        updateEnabled: true,
      }),
    });

    if (r.status === 201 || r.status === 204) {
      return res.status(200).json({ ok: true });
    }
    if (r.status === 400) {
      const data = await r.json();
      // already exists = success for the user
      if (data.code === 'duplicate_parameter') return res.status(200).json({ ok: true });
      return res.status(400).json({ error: data.message });
    }
    return res.status(500).json({ error: 'Erro ao cadastrar' });
  } catch (e) {
    return res.status(500).json({ error: 'Erro interno' });
  }
}
