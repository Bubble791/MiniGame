/*********** ITEM SPRITE TAGS ************/
#define TAG_ITEM_HEARTSCALE     14
#define TAG_ITEM_HARDSTONE      15
#define TAG_ITEM_REVIVE         16
#define TAG_ITEM_STAR_PIECE     17
#define TAG_ITEM_DAMP_ROCK      18
#define TAG_ITEM_RED_SHARD      19
#define TAG_ITEM_BLUE_SHARD     20
#define TAG_ITEM_IRON_BALL      21
#define TAG_ITEM_REVIVE_MAX     22
#define TAG_ITEM_EVER_STONE     23

#define TAG_STONE_1X4           24
#define TAG_STONE_4X1           25
#define TAG_STONE_2X4           26
#define TAG_STONE_4X2           27
#define TAG_STONE_2X2           28
#define TAG_STONE_3X3           29

/*********** DEBUG SWITCHES ************/
// #define DEBUG_ITEM_GEN

#define SELECTED          0
#define DESELECTED        255
#define ITEM_TILE_NONE    0
#define ITEM_TILE_DUG_UP  5
#define MAX_NUM_BURIED_ITEMS 4

/*********** ITEM/STONE IDS ************/
#define ITEMID_NONE                     0
#define ITEMID_HARD_STONE               1
#define ITEMID_REVIVE                   2
#define ITEMID_STAR_PIECE               3
#define ITEMID_DAMP_ROCK                4
#define ITEMID_RED_SHARD                5
#define ITEMID_BLUE_SHARD               6
#define ITEMID_IRON_BALL                7
#define ITEMID_REVIVE_MAX               8
#define ITEMID_EVER_STONE               9
#define ITEMID_HEART_SCALE              10

#define ID_STONE_1x4                    250
#define ID_STONE_4x1                    251
#define ID_STONE_2x4                    252
#define ID_STONE_4x2                    253
#define ID_STONE_2x2                    254
#define ID_STONE_3x3                    255

enum {
    COPYWIN_NONE,
    COPYWIN_MAP,
    COPYWIN_GFX,
    COPYWIN_FULL,
};

#define TEXT_COLOR_TRANSPARENT  0x0
#define TEXT_COLOR_WHITE        0x1
#define TEXT_COLOR_DARK_GRAY    0x2
#define TEXT_COLOR_LIGHT_GRAY   0x3
#define TEXT_COLOR_RED          0x4
#define TEXT_COLOR_LIGHT_RED    0x5
#define TEXT_COLOR_GREEN        0x6
#define TEXT_COLOR_LIGHT_GREEN  0x7
#define TEXT_COLOR_BLUE         0x8
#define TEXT_COLOR_LIGHT_BLUE   0x9
#define TEXT_DYNAMIC_COLOR_1    0xA // Usually white
#define TEXT_DYNAMIC_COLOR_2    0xB // Usually white w/ tinge of green
#define TEXT_DYNAMIC_COLOR_3    0xC // Usually white
#define TEXT_DYNAMIC_COLOR_4    0xD // Usually aquamarine
#define TEXT_DYNAMIC_COLOR_5    0xE // Usually blue-green
#define TEXT_DYNAMIC_COLOR_6    0xF // Usually cerulean

#define ITEM_NONE   0

/////////////////////////////////////////////////修改
#define ITEM_HARD_STONE 1
#define ITEM_REVIVE 2
#define ITEM_STAR_PIECE 3
#define ITEM_WATER_STONE 4
#define ITEM_RED_SHARD 5
#define ITEM_BLUE_SHARD 6
#define ITEM_ULTRA_BALL 7
#define ITEM_MAX_REVIVE 8
#define ITEM_EVERSTONE 9
#define ITEM_HEART_SCALE 10