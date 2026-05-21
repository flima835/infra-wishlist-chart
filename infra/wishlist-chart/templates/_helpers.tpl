{{/*
Nome base usado em todos os recursos do chart.
Limita a 63 caracteres (limite do DNS do Kubernetes).
*/}}
{{- define "wishlist.name" -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Labels padrão aplicados a todos os recursos.
*/}}
{{- define "wishlist.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ include "wishlist.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Labels de seleção (selector) — imutáveis após criação.
*/}}
{{- define "wishlist.selectorLabels" -}}
app.kubernetes.io/name: {{ include "wishlist.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
