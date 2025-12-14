"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { register, login, saveTokens, saveUser, ApiError } from "@/lib/api"
import { AlertCircle, Loader2, CheckCircle2 } from "lucide-react"

export function RegisterForm() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    senha: "",
    confirmSenha: "",
    cidade: "",
  })
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    // Validações básicas
    if (!formData.username.trim() || !formData.email.trim() || !formData.senha.trim() || !formData.cidade.trim()) {
      setError("Por favor, preencha todos os campos obrigatórios")
      return
    }

    if (formData.senha !== formData.confirmSenha) {
      setError("As senhas não coincidem")
      return
    }

    if (formData.senha.length < 6) {
      setError("A senha deve ter no mínimo 6 caracteres")
      return
    }

    if (!formData.email.includes("@")) {
      setError("Por favor, insira um e-mail válido")
      return
    }

    setIsLoading(true)

    try {
      // Criar conta (todos começam como participante)
      const usuario = await register({
        username: formData.username,
        email: formData.email,
        senha: formData.senha,
        cidade: formData.cidade,
        papel: "participante",
      })

      // Após criar conta, fazer login automaticamente
      const loginResponse = await login({
        username: formData.username,
        password: formData.senha,
      })

      // Salvar tokens e dados do usuário
      saveTokens(loginResponse.access, loginResponse.refresh)
      saveUser(loginResponse.usuario)

      // Redirecionar para dashboard
      router.push("/dashboard")
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.status === 400) {
          setError("Este nome de usuário ou e-mail já está em uso")
        } else if (err.status === 0) {
          setError("Não foi possível conectar ao servidor. Verifique se o backend está rodando.")
        } else {
          setError(err.message)
        }
      } else {
        setError("Ocorreu um erro inesperado. Tente novamente.")
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <div className="space-y-2">
        <Label htmlFor="username">
          Nome de usuário <span className="text-destructive">*</span>
        </Label>
        <Input
          id="username"
          name="username"
          type="text"
          placeholder="Digite seu nome de usuário"
          value={formData.username}
          onChange={handleChange}
          disabled={isLoading}
          autoComplete="username"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="email">
          E-mail <span className="text-destructive">*</span>
        </Label>
        <Input
          id="email"
          name="email"
          type="email"
          placeholder="seu@email.com"
          value={formData.email}
          onChange={handleChange}
          disabled={isLoading}
          autoComplete="email"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="cidade">
          Cidade <span className="text-destructive">*</span>
        </Label>
        <Input
          id="cidade"
          name="cidade"
          type="text"
          placeholder="Digite sua cidade"
          value={formData.cidade}
          onChange={handleChange}
          disabled={isLoading}
          autoComplete="address-level2"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="senha">
          Senha <span className="text-destructive">*</span>
        </Label>
        <Input
          id="senha"
          name="senha"
          type="password"
          placeholder="Mínimo 6 caracteres"
          value={formData.senha}
          onChange={handleChange}
          disabled={isLoading}
          autoComplete="new-password"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="confirmSenha">
          Confirmar senha <span className="text-destructive">*</span>
        </Label>
        <Input
          id="confirmSenha"
          name="confirmSenha"
          type="password"
          placeholder="Digite a senha novamente"
          value={formData.confirmSenha}
          onChange={handleChange}
          disabled={isLoading}
          autoComplete="new-password"
          required
        />
      </div>

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Criando conta...
          </>
        ) : (
          <>
            <CheckCircle2 className="mr-2 h-4 w-4" />
            Criar conta
          </>
        )}
      </Button>

      <p className="text-center text-sm text-muted-foreground">
        Já tem uma conta?{" "}
        <a href="/login" className="font-medium text-primary hover:underline">
          Faça login
        </a>
      </p>
    </form>
  )
}
