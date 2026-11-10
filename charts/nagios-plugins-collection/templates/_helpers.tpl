{{/*
SPDX-FileCopyrightText: 2025 Thomas Vincent
SPDX-License-Identifier: Apache-2.0
*/}}
{{- define "nagios-plugins-collection.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "nagios-plugins-collection.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "nagios-plugins-collection.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{- default (include "nagios-plugins-collection.fullname" .) .Values.serviceAccount.name -}}
{{- else -}}
{{- default "default" .Values.serviceAccount.name -}}
{{- end -}}
{{- end -}}

{{/*
The container image: repository@digest when image.digest is set (the tag is
then ignored, since the digest alone selects the image), else repository:tag.
*/}}
{{- define "nagios-plugins-collection.image" -}}
{{- $image := .Values.image -}}
{{- with $image.digest -}}
{{- if not (regexMatch "^sha256:[0-9a-f]{64}$" .) -}}
{{- fail (printf "image.digest must be sha256: followed by 64 lowercase hex digits, got %q" .) -}}
{{- end -}}
{{- printf "%s@%s" $image.repository . -}}
{{- else -}}
{{- printf "%s:%s" $image.repository ($image.tag | default $.Chart.AppVersion) -}}
{{- end -}}
{{- end -}}
