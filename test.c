#include <sys/types.h>
#include <time.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>

#define X_GETTIME(ts) \
    do { ts.tv_sec = 0; ts.tv_nsec= 0; clock_gettime(CLOCK_MONOTONIC, &ts); } while(0)

#define X_DIFF(s, e) \
    (((double)ts_end.tv_sec + 1.0e-9*ts_end.tv_nsec) - \
    ((double)ts_start.tv_sec + 1.0e-9*ts_start.tv_nsec))

int main(int argc, char **argv)
{
    struct timespec ts_start, ts_end;
    double elapse[NB_TEST], sum;

    for (int cn = 0; cn < NB_TEST; cn++) {

        X_GETTIME(ts_start);

	static const uint8_t key[16] = {}, iv[12] = {}, aad[13] = {}, text[16384] = {};
	//ptls_fusion_aesgcm_context_t ctx;
	uint8_t encrypted[sizeof(text) + 16];
	size_t textlen = 16384;

	// 以下のifを追加すると0.7秒遅くなる
#if USE_SCANF == 1
        if (sscanf(argv[1], "%zu", &textlen) != 1) {
            fprintf(stderr, "failed to obtain text length from argument\n");
            return 1;
        }
#endif

	//ptls_fusion_aesgcm_init(&ctx, key);

	for (int i = 0; i < 1000000; ++i) {
            usleep(1);
	    //ptls_fusion_aesgcm_encrypt(&ctx, iv, aad, sizeof(aad), encrypted, text, textlen);
	}

        X_GETTIME(ts_end);

	// このprintfにはバグがあり、sizeof(text)をtextlenに変えると、上掲の速度低下はなくなる
#if USE_SIZEOF == 1
        for (int i = 0; i < 16; ++i)
            printf("%02x", encrypted[sizeof(text) + i]);
#else
        for (int i = 0; i < 16; ++i)
            printf("%02x", encrypted[textlen + i]);
#endif
        printf("\n");

        elapse[cn] = X_DIFF(ts_end, ts_start);
    }

    sum = 0;
    for (int cn = 0; cn < NB_TEST; cn++) {
        sum += elapse[cn];
        //fprintf(stderr, "elapse: %lf\n", elapse[cn]);
    }
    fprintf(stderr, "elapse: %lf\n", sum / NB_TEST);

    return 0;
	return 0;
}
