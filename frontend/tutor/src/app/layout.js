/* Configurações de layout */ 

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <head>
        <title>Tutor</title>
      </head>
      <body>
        {children}
      </body>
    </html>
  );
}