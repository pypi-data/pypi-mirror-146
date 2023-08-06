#pragma once

#include "../serialisation/serialisation_impl_fwd.h"
#include "../util/iterator_facade.h"
#include "bit_decoder.h"
#include "chunk_file_cache.h"

#include <limits>

class ChunkReference;
class Encoder;

struct RawSample {
    int64_t timestamp;
    double value;
};

bool operator==(const RawSample& a, const RawSample& b);
bool operator!=(const RawSample& a, const RawSample& b);

struct Sample : public RawSample {
    static constexpr uint16_t noBitWidth = std::numeric_limits<uint16_t>::max();
    struct {
        // The first two sample timestamps are not encoded as delta-of-deltas.
        // avoid including them in the minimal bit width breakdown.
        uint16_t minTimestampBitWidth = noBitWidth;
        uint16_t timestampBitWidth = 0;
        uint16_t valueBitWidth = 0;
    } meta;
};

struct SampleIterator : public iterator_facade<SampleIterator, Sample> {
    SampleIterator() = default;
    SampleIterator(Decoder& dec, size_t sampleCount, bool rawChunk = false);

    void increment();
    const Sample& dereference() const {
        return s;
    }

    bool is_end() const {
        return currentIndex == sampleCount;
    }

private:
    double readValue();

    /// return new TS, and raw DOD
    std::pair<int64_t, int64_t> readTS();
    int64_t readTSDod();

    struct {
        int64_t ts = 0;
        int64_t tsDelta = 0;
        double value = 0;
        uint8_t leading = 0;
        uint8_t trailing = 0;
    } prev;
    ssize_t currentIndex = -1;
    size_t sampleCount;
    Decoder* dec;
    BitDecoder bits;

    bool rawChunk = false;

    Sample s;
};

// non-copying type. Holds a shared_ptr to the resource to ensure it
// lives as long as it is being used.
class ChunkView {
public:
    ChunkView() = default;
    ChunkView(ChunkFileCache& cfc, const ChunkReference& chunkRef);

    SampleIterator samples() {
        return {dec, sampleCount, rawChunk};
    }

    size_t dataLen;
    size_t dataOffset;

    size_t sampleCount;

private:
    friend void pdu::detail::serialise_impl(Encoder& e, const ChunkView& cv);
    // offset into the resource to the chunk start
    size_t baseOffset;
    std::shared_ptr<Resource> res;
    Decoder dec;
    bool rawChunk = false;
};