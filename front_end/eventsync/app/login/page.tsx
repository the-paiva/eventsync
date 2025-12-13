import { LoginForm } from "@/components/login-form"
import { Calendar } from "lucide-react"

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-muted/30 to-background p-4">
      <div className="w-full max-w-md">
        {/* Logo e Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-2xl mb-4">
            <Calendar className="w-8 h-8 text-primary-foreground" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-balance">Bem-vindo ao EventSync</h1>
          <p className="text-muted-foreground mt-2 text-balance">Faça login para gerenciar seus eventos</p>
        </div>

        {/* Card do Formulário */}
        <div className="bg-card border border-border rounded-xl shadow-lg p-6 md:p-8">
          <LoginForm />
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-muted-foreground mt-6">
          Ao fazer login, você concorda com nossos Termos de Uso e Política de Privacidade
        </p>
      </div>
    </div>
  )
}
