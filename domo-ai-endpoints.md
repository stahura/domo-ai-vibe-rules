# Rule: Domo App Platform AI Endpoints

You are building a Domo Custom App that needs to use AI/ML capabilities. Domo provides AI endpoints for text generation and image-to-text (OCR).

## Prerequisites
- The domo.js library must be available (included automatically when running in Domo)
- AI features must be enabled for your Domo instance
- For local development, use `@domoinc/ryuu-proxy` to proxy API calls

---

## Text Generation API

### Basic text generation
```javascript
const prompt = 'Tell me a joke about data.';

domo.post('/domo/ai/v1/text/generation', {
  input: prompt
})
  .then(response => {
    console.log(response.choices[0].output);
  });
```

### Response format
```json
{
  "prompt": "Tell me a joke about data.",
  "choices": [
    {
      "output": "Why did the data scientist break up with the statistician? Because they found someone more significant!"
    }
  ],
  "modelId": "8dc5737d-0bc8-425b-ad0d-5d6ec1a99e72",
  "isCustomerModel": true
}
```

### With async/await
```javascript
async function generateText(prompt) {
  try {
    const response = await domo.post('/domo/ai/v1/text/generation', {
      input: prompt
    });
    return response.choices[0].output;
  } catch (error) {
    console.error('AI generation error:', error);
    throw error;
  }
}

// Example usage
const joke = await generateText('Tell me a joke about data.');
console.log(joke);
```

### Optional parameters
The body can include additional optional parameters:
- `model` - Specific model ID (omit to use the latest default model)
- `promptTemplate` - Template for structured prompts
- `parameters` - Parameters to inject into the template
- `system` - System prompt for context/behavior

For most use cases, just passing `{ input: prompt }` is sufficient.

---

## Image to Text API (OCR)

### Basic image-to-text
```javascript
async function imageToText(base64Image) {
  // Remove data URL prefix if present
  let pureBase64 = base64Image;
  if (pureBase64.startsWith('data:')) {
    pureBase64 = pureBase64.substring(pureBase64.indexOf(',') + 1);
  }

  const response = await domo.post('/domo/ai/v1/image/text', {
    input: 'Return the text in the image, ensuring new lines are preserved',
    image: {
      mediaType: 'image/png',
      type: 'base64',
      data: pureBase64
    }
  });

  return response.choices[0].output;
}
```

### With system prompt for detailed instructions
```javascript
async function imageToText(base64Image) {
  let pureBase64 = base64Image;
  if (pureBase64.startsWith('data:')) {
    pureBase64 = pureBase64.substring(pureBase64.indexOf(',') + 1);
  }

  const response = await domo.post('/domo/ai/v1/image/text', {
    input: 'Return the text in the image',
    image: {
      mediaType: 'image/png',
      type: 'base64',
      data: pureBase64
    },
    system: `You are an AI assistant performing OCR on an image.
Examine the entire image and transcribe all visible text exactly as it appears.
Maintain original spelling, capitalization, punctuation, and line structure.`
  });

  return response.choices[0].output;
}
```

Key points:
- Endpoint: `/domo/ai/v1/image/text`
- Strip data URL prefix (`data:image/png;base64,`) before sending
- `mediaType` should match the image format (e.g., `image/png`, `image/jpeg`)
- `model` is optional - omit to use the latest default model

---

## Common Patterns

### React hook for AI text generation
```javascript
import { useState, useCallback } from 'react';

function useAIGeneration() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generate = useCallback(async (prompt) => {
    setLoading(true);
    setError(null);

    try {
      const response = await domo.post('/domo/ai/v1/text/generation', {
        input: prompt
      });
      return response.choices[0].output;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { generate, loading, error };
}

// Usage
function MyComponent() {
  const { generate, loading, error } = useAIGeneration();

  const handleClick = async () => {
    const result = await generate('Summarize this data trend...');
    console.log(result);
  };

  return (
    <button onClick={handleClick} disabled={loading}>
      {loading ? 'Generating...' : 'Generate'}
    </button>
  );
}
```

### AI service
```javascript
// services/ai.js
export const aiService = {
  async generateText(prompt) {
    const response = await domo.post('/domo/ai/v1/text/generation', {
      input: prompt
    });
    return response.choices[0].output;
  },

  async imageToText(base64Image) {
    let pureBase64 = base64Image;
    if (pureBase64.startsWith('data:')) {
      pureBase64 = pureBase64.substring(pureBase64.indexOf(',') + 1);
    }

    const response = await domo.post('/domo/ai/v1/image/text', {
      input: 'Return the text in the image',
      image: {
        mediaType: 'image/png',
        type: 'base64',
        data: pureBase64
      }
    });
    return response.choices[0].output;
  }
};
```

### Error handling with retry
```javascript
async function generateWithRetry(prompt, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await domo.post('/domo/ai/v1/text/generation', {
        input: prompt
      });
      return response.choices[0].output;
    } catch (error) {
      if (attempt === maxRetries) throw error;

      // Exponential backoff
      await new Promise(resolve =>
        setTimeout(resolve, Math.pow(2, attempt) * 1000)
      );
    }
  }
}
```

---

## Best Practices

1. **Keep prompts clear and specific**
   - Be direct about what you want
   - Provide context when needed

2. **Handle responses gracefully**
   - Always check for `choices[0].output`
   - Implement error handling

3. **User Experience**
   - Show loading states during generation
   - Provide feedback on errors
   - Consider streaming for long responses if available

4. **Performance**
   - Cache results when appropriate
   - Don't send unnecessarily large images
   - Implement retry logic for reliability

---

## Checklist
- [ ] AI features enabled for your Domo instance
- [ ] Using correct endpoint (`/domo/ai/v1/text/generation` or `/domo/ai/v1/image/text`)
- [ ] Body includes `input` with prompt
- [ ] For images: base64 data URL prefix stripped, correct `mediaType`
- [ ] Response handled correctly (`response.choices[0].output`)
- [ ] Error handling implemented
- [ ] Loading states shown in UI
- [ ] Retry logic for reliability (optional)
