import express, {Request ,Response ,NextFunction} from 'express';
import jwt from 'jsonwebtoken';
import path from 'path';

const app = express();
const jwt_chave = 'seu_segredo_aqui';

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

app.get('/', (req,res)=>{
    res.sendFile(path.join(__dirname, './pages/log.html'));
})