# Imagen base de Node.js
FROM node:18

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY package.json package-lock.json ./
RUN npm install

COPY . .

# Construir la aplicación
RUN npm run build

# Instalar un servidor estático para servir la aplicación
RUN npm install -g serve

# Exponer el puerto para la aplicación
EXPOSE 5173

# Comando para ejecutar el servidor estático
CMD ["serve", "-s", "dist", "-l", "5173"]
