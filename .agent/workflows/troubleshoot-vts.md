---
description: Troubleshoot VTube Studio API connection when commands execute but model doesn't move
---

# VTube Studio Troubleshooting Workflow

## Step 1: Verify VTube Studio API is Enabled

1. Open **VTube Studio**
2. Click the **gear icon** (Settings) in the bottom right
3. Navigate to **"Plugins"** tab on the left sidebar
4. Find **"Start API"** checkbox and ensure it's **CHECKED** ✓
5. Verify the port is **8001** (should show below the checkbox)
6. If you changed anything, click **"Save"** at the bottom

**Expected result:** API should show as "Running" with green indicator

---

## Step 2: Check Plugin Authorization

### First Time Setup

When you run the script for the first time, VTube Studio should show a popup:

```
Plugin Authorization Request
Plugin: "Llama Live2D Controller"
Developer: "YourName"
[Allow] [Deny]
```

**If you see this popup:**
- Click **"Allow"**
- The script will save a token to `vts_token.txt`

**If you DON'T see the popup:**
- You may have denied it previously
- Go to Step 2b to reset

### Step 2b: Reset Plugin Authorization

1. In VTube Studio, go to **Settings > Plugins**
2. Scroll down to **"Allowed Plugins"** section
3. Look for **"Llama Live2D Controller"**
4. If it exists: Click the **trash/delete icon** next to it
5. Delete the file: `d:\aigirlfriend\vts_token.txt`
6. Re-run your command:
   ```bash
   python main_multi_model.py --model chino11 --emotion happy
   ```
7. The authorization popup should appear again
8. Click **"Allow"**

---

## Step 3: CRITICAL - Model Parameter Mismatch Check

**This is the most common issue!**

### The Problem:
Your script sends chino11-specific parameters like `PARAM_ANGLE_X`, `PARAM_MOUTH_FORM`, etc.

**But if a DIFFERENT model is loaded in VTS, those parameters don't exist!**

### Solution:

**Option A: Load the chino11 model in VTube Studio**

1. In VTube Studio, click **"Model"** button (top left)
2. Browse to where you have the chino11 model
3. Load: `chino11.vrm` or the chino11 Live2D model files
4. Make sure it's the SAME model you analyzed

**Option B: Use a different model that's currently loaded**

If you want to use a different model currently in VTS:

1. Find out which model is loaded (check VTS model name)
2. Analyze that model instead:
   ```bash
   # Copy that model's folder to d:\yourmodel
   # Then create a new model config for it
   ```

---

## Step 4: Verify Active Model in VTS

1. Look at the **top of VTube Studio window**
2. You should see the model name (e.g., "chino11" or something else)
3. **The model name must match what you're controlling**

**Test with a generic parameter:**

Run this test to see if ANY parameter works:

```bash
python main_multi_model.py --model chino11 --emotion neutral
```

If even `neutral` doesn't work, it's a parameter mismatch.

---

## Step 5: Enable Verbose Logging (Debug Mode)

Add debug output to see what's being sent:

### Quick Debug Test

Run this command in Python to test directly:

```bash
cd d:\aigirlfriend
python
```

Then in the Python REPL:

```python
import asyncio
import websockets
import json

async def test_vts():
    ws = await websockets.connect("ws://localhost:8001")
    
    # Test 1: Get API state
    msg = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "test",
        "messageType": "APIStateRequest"
    }
    await ws.send(json.dumps(msg))
    response = await ws.recv()
    print("API State:", json.loads(response))
    
    # Test 2: Get current model
    msg["messageType"] = "CurrentModelRequest"
    await ws.send(json.dumps(msg))
    response = await ws.recv()
    model_info = json.loads(response)
    print("Current Model:", model_info["data"]["modelName"])
    print("Model ID:", model_info["data"]["modelID"])

asyncio.run(test_vts())
```

**This will show:**
- If VTS API is running
- What model is currently loaded
- If the connection works at all

---

## Step 6: Test with VTube Studio's Built-in Parameters

Most Live2D models have these STANDARD parameters:

```bash
# Test with common/standard parameters
# Create a test file: test_generic.py
```

```python
import asyncio
import websockets
import json

async def test_generic_params():
    async with websockets.connect("ws://localhost:8001") as ws:
        # Simple head tilt - works on most models
        msg = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "test",
            "messageType": "InjectParameterDataRequest",
            "data": {
                "faceFound": True,
                "mode": "set",
                "parameterValues": [
                    {"id": "FaceAngleX", "value": 10.0},  # Try standard name
                    {"id": "FaceAngleY", "value": 5.0}
                ]
            }
        }
        await ws.send(json.dumps(msg))
        response = await ws.recv()
        print(json.loads(response))

asyncio.run(test_generic_params())
```

---

## Step 7: Get Available Parameters from Current Model

Run this to see what parameters the CURRENTLY LOADED model actually has:

```python
import asyncio
import websockets
import json

async def get_available_params():
    async with websockets.connect("ws://localhost:8001") as ws:
        msg = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "test",
            "messageType": "ParameterListRequest"
        }
        await ws.send(json.dumps(msg))
        response = await ws.recv()
        data = json.loads(response)
        
        print("Available parameters:")
        for param in data["data"]["parameters"]:
            print(f"  {param['name']} (min: {param['min']}, max: {param['max']})")

asyncio.run(get_available_params())
```

**Compare the output with chino11's expected parameters!**

---

## Common Issues & Solutions

### Issue 1: "Connected!" but no movement
**Cause:** Parameter name mismatch  
**Solution:** Load chino11 model in VTS, or create new model config

### Issue 2: "Connection Refused"
**Cause:** VTS API not enabled or wrong port  
**Solution:** Enable API in VTS settings (Step 1)

### Issue 3: "Authentication Failed"
**Cause:** Token expired or denied  
**Solution:** Delete vts_token.txt and re-authorize (Step 2b)

### Issue 4: Model moves but wrong parts
**Cause:** Different model with similar but not exact parameters  
**Solution:** Analyze the current model's parameters (Step 7)

---

## Quick Verification Checklist

- [ ] VTube Studio is open
- [ ] API is enabled (Settings > Plugins > Start API ✓)
- [ ] Port is 8001
- [ ] Plugin "Llama Live2D Controller" is in Allowed Plugins list
- [ ] chino11 model is loaded in VTS (check top of window)
- [ ] Script shows "Connected!" message
- [ ] vts_token.txt exists in d:\aigirlfriend\

---

## Next Steps After Connection Works

Once you get movement:

1. Test all tiers:
   ```bash
   python main_multi_model.py --model chino11 --emotion happy
   python main_multi_model.py --model chino11 --micro smirk
   python main_multi_model.py --model chino11 --composite sarcastic
   ```

2. Fine-tune parameter values in `models/chino11.py` if expressions don't look right

3. Proceed with voice chat integration
