<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { Primitive } from 'reka-ui'
import { cn } from '@/lib/utils'

interface Props {
  variant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'ghost'
  class?: HTMLAttributes['class']
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
})

const variantClasses = {
  default: 'bg-primary text-primary-foreground',
  secondary: 'bg-secondary text-secondary-foreground',
  destructive: 'bg-destructive text-destructive-foreground',
  outline: 'border border-input bg-background',
  ghost: 'hover:bg-accent hover:text-accent-foreground',
}
</script>

<template>
  <Primitive
    :class="cn(
      'inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium transition-colors',
      variantClasses[variant],
      props.class
    )"
  >
    <slot />
  </Primitive>
</template>