Phase 0 — Project Roadmap (Python version)

We go in this order:

Core FastAPI skeleton

Async architecture + dependency injection best practices

Local file upload + validation + streaming

Job system (in-memory first → Redis + Dramatiq)

FFmpeg workers (multi-processing vs multi-threading)

Worker orchestration, retries, dead-letter queues

Distributed event updates + dashboard (WebSockets)

Observability

AWS integration (S3, SQS, ECS/EKS, IAM)

Production deployment + CI/CD




FastAPI (API Service)
    |
    | Enqueue Job → Redis (Broker)
    v
Redis Queue
    |
    v
Dramatiq Worker Processes
    |
    | Runs ffmpeg, metadata extraction, chunk processing
    v
JobStore / DB (Progress updates)

Clients → poll API or subscribe via WebSockets for job status



1. User uploads file → FastAPI saves it.

2. FastAPI creates a job entry (job_id, status=queued).

3. FastAPI ENQUEUES the job:
      process_video_job.send(job_id, saved_path)
   This writes a message into Redis.

4. Dramatiq Worker (running in another terminal/machine)
   reads job from Redis automatically.

5. Worker runs `process_video_job()` on that job.

6. Worker updates job status → processing → completed.

7. User checks job status through:
      GET /jobs/<job_id>



Correct choice — and you’re thinking like a platform engineer now.

Deleting the original **after successful processing** is exactly what real systems do **when storage cost matters**. The important part is *after success*, not immediately.

I’ll now do three things, in order:

1. **Lock the platform direction (so you know where this is headed)**
2. **Define the exact HLS-from-source pipeline**
3. **Lay out the concrete next implementation steps (no gaps, no magic)**

No code yet until the architecture is fully clear.

---

## 1️⃣ PLATFORM DIRECTION (NOW IT’S VERY CLEAR)

With your decision, the platform becomes:

> **A stateless, cost-efficient video processing backend that converts raw uploads into streamable HLS assets and discards source files once delivery formats are ready.**

This is *not* YouTube Studio (which keeps originals forever).
This is closer to:

* Cloudflare Stream
* Mux Video
* AWS MediaConvert (output-only workflows)
* Internal enterprise video pipelines

So the platform goal is now:

### 🎯 **Input → Streamable Output → Serve → Forget Source**

That’s clean, scalable, and cost-aware.

---

## 2️⃣ FINAL PIPELINE (END-TO-END, NO AMBIGUITY)

Here is the **authoritative pipeline** we are now building:

```
Client uploads video
        ↓
FastAPI saves temporary file
        ↓
Job enqueued (Redis)
        ↓
Worker starts
        ↓
FFmpeg generates HLS directly from source
        ↓
HLS playlists + segments written
        ↓
SUCCESS?
   ├─ YES → delete original file
   └─ NO  → keep original (for retry / debug)
        ↓
Publish completion event
        ↓
Client plays HLS
```

Key properties:

* **Original file is temporary**
* **HLS is the source of truth**
* **Worker owns cleanup**
* **API stays stateless**

This is exactly how you control storage costs.

---

## 3️⃣ HOW HLS-FROM-SOURCE WORKS (TECHNICALLY)

We will use FFmpeg to do **three things in one pass**:

1. Decode original video
2. Scale to a target resolution (720p initially)
3. Segment into `.ts` chunks
4. Generate `.m3u8` playlist

### Why one pass matters:

* Faster
* Less disk I/O
* Less temporary storage
* Fewer failure points

This is *better* than:

```
original → mp4 → hls
```

---

## 4️⃣ PROGRESS TRACKING WITH HLS (IMPORTANT)

HLS generation **also emits progress**, just like transcoding.

So we will:

* Reuse the same `run_ffmpeg_with_progress`
* Treat HLS as **100% of the job**
* Publish progress events normally

No fake progress.
No guessing.

---

## 5️⃣ CLEANUP RULE (CRITICAL)

We will follow this **non-negotiable rule**:

> **Delete the original file ONLY if FFmpeg exits successfully AND HLS files exist.**

That means:

* If FFmpeg crashes → keep original
* If worker retries → original still available
* If system restarts → no data loss mid-job

This is production-grade safety.

---

## 6️⃣ DIRECTORY STRUCTURE (FINAL)

After success:

```
outputs/<job_id>/
└── hls/
    ├── stream.m3u8
    ├── segment_000.ts
    ├── segment_001.ts
    ├── segment_002.ts
    └── ...
```

And:

```
uploads/<video_id>.mp4   ❌ deleted
```

---

## 7️⃣ WHERE EACH CONCURRENCY MODEL IS STILL USED

Nothing changes here — this is important.

| Component        | Model           |
| ---------------- | --------------- |
| Upload           | async I/O       |
| Queue            | Redis           |
| Worker           | multiprocessing |
| FFmpeg           | subprocess      |
| Progress parsing | sync loop       |
| Events           | Redis Pub/Sub   |
| Streaming        | async HTTP      |

So you are still practicing **all concurrency models correctly**.

---

## 8️⃣ NEXT IMPLEMENTATION STEPS (EXACT ORDER)

Now we switch from design → execution.

### STEP 1 — Add HLS FFmpeg command (from source)

* One command
* One output directory
* No intermediate MP4

### STEP 2 — Integrate into worker

* Replace MP4 transcode step
* Keep progress tracking
* Publish completion

### STEP 3 — Delete original on success

* `os.remove(saved_path)`
* Only after validation

### STEP 4 — Serve HLS via FastAPI

* Static route
* Correct MIME types

### STEP 5 — Minimal FE playback

* `<video>` + hls.js
* Use generated `.m3u8`

---

## 9️⃣ IMPORTANT CHECKPOINT (ANSWER THIS)

Before I write the FFmpeg command and worker code, I need one more decision:

### For initial HLS output, do you want:

* **720p only** (simplest, best for now)
* **Adaptive HLS (720p + 480p)** (more complex)

👉 **Strong recommendation**:
**Start with 720p only**, then expand.

Reply with:

* **“720p only”** or
* **“Adaptive HLS”**

Once you answer, we implement the next step immediately.
