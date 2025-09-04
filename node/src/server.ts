import express, {Request ,Response ,NextFunction} from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import jwt from 'jsonwebtoken';
import path from 'path';

const app = express();
const jwt_chave = 'seu_segredo_aqui';

const PORT = 3000;

app.use(express.static(path.join(__dirname, '../public')));

interface autentica_req extends Request {
  usuario?: string|jwt.JwtPayload;
}

const middleware_auth = (req: autentica_req, res: Response, next: NextFunction) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).send('Acesso negado');
  }

  jwt.verify(token, jwt_chave, (err, user) => {
    if (err) {
      return res.status(403).send('Token inválido');
    }
    req.usuario = user;
    next();
  });
};



app.use('/logar', createProxyMiddleware({
  target: 'http://servico-python:5000',
  changeOrigin: true,
  pathRewrite: {
      '^/logar': '',
  },
}));

app.listen(PORT, () => {
  console.log(`navegador rodando: http://127.0.0.1:3000 `);
  console.log(`servidor rodando: http://localhost:${PORT}`);
});