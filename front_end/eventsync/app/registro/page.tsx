import { RegisterForm } from "@/components/auth/register-form"
import { Calendar } from "lucide-react"


export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-muted/30 to-background p-4">
      <div className="w-full max-w-md">
        {/* Logo e Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-2xl mb-4">
            <Calendar className="w-8 h-8 text-primary-foreground" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-balance">Crie sua conta</h1>
          <p className="text-muted-foreground mt-2 text-balance">Comece a gerenciar eventos de forma inteligente</p>
        </div>

        {/* Card do Formulário */}
        <div className="bg-card border border-border rounded-xl shadow-lg p-6 md:p-8">
          <RegisterForm />
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-muted-foreground mt-6 text-balance">
          Ao criar uma conta, você concorda com nossos Termos de Uso e Política de Privacidade
        </p>
      </div>
    </div>
  )
}
