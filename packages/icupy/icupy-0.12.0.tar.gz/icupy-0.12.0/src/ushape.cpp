#include "main.hpp"
#include <unicode/ushape.h>

using namespace icu;

void init_ushape(py::module &m) {
  m.def(
      "u_shape_arabic",
      [](const char16_t *source, int32_t source_length, uint32_t options) {
        ErrorCode error_code;
        auto dest_size = u_shapeArabic(source, source_length, nullptr, 0, options, error_code);
        std::u16string result(dest_size, u'\0');
        error_code.reset();
        u_shapeArabic(source, source_length, result.data(), dest_size, options, error_code);
        if (error_code.isFailure()) {
          throw ICUError(error_code);
        }
        return result;
      },
      py::arg("source"), py::arg("source_length"), py::arg("options"));

  // Tashkeel aggregation options
  m.attr("U_SHAPE_AGGREGATE_TASHKEEL") = U_SHAPE_AGGREGATE_TASHKEEL;
  m.attr("U_SHAPE_AGGREGATE_TASHKEEL_MASK") = U_SHAPE_AGGREGATE_TASHKEEL_MASK;
  m.attr("U_SHAPE_AGGREGATE_TASHKEEL_NOOP") = U_SHAPE_AGGREGATE_TASHKEEL_NOOP;

  // Digit type options
  m.attr("U_SHAPE_DIGIT_TYPE_AN") = U_SHAPE_DIGIT_TYPE_AN;
  m.attr("U_SHAPE_DIGIT_TYPE_AN_EXTENDED") = U_SHAPE_DIGIT_TYPE_AN_EXTENDED;
  m.attr("U_SHAPE_DIGIT_TYPE_MASK") = U_SHAPE_DIGIT_TYPE_MASK;
  m.attr("U_SHAPE_DIGIT_TYPE_RESERVED") = U_SHAPE_DIGIT_TYPE_RESERVED;

  // Digit shaping options
  m.attr("U_SHAPE_DIGITS_ALEN2AN_INIT_AL") = U_SHAPE_DIGITS_ALEN2AN_INIT_AL;
  m.attr("U_SHAPE_DIGITS_ALEN2AN_INIT_LR") = U_SHAPE_DIGITS_ALEN2AN_INIT_LR;
  m.attr("U_SHAPE_DIGITS_AN2EN") = U_SHAPE_DIGITS_AN2EN;
  m.attr("U_SHAPE_DIGITS_EN2AN") = U_SHAPE_DIGITS_EN2AN;
  m.attr("U_SHAPE_DIGITS_MASK") = U_SHAPE_DIGITS_MASK;
  m.attr("U_SHAPE_DIGITS_NOOP") = U_SHAPE_DIGITS_NOOP;
  m.attr("U_SHAPE_DIGITS_RESERVED") = U_SHAPE_DIGITS_RESERVED;

  // Memory options
  m.attr("U_SHAPE_LAMALEF_AUTO") = U_SHAPE_LAMALEF_AUTO;
  m.attr("U_SHAPE_LAMALEF_BEGIN") = U_SHAPE_LAMALEF_BEGIN;
  m.attr("U_SHAPE_LAMALEF_END") = U_SHAPE_LAMALEF_END;
  m.attr("U_SHAPE_LAMALEF_MASK") = U_SHAPE_LAMALEF_MASK;
  m.attr("U_SHAPE_LAMALEF_NEAR") = U_SHAPE_LAMALEF_NEAR;
  m.attr("U_SHAPE_LAMALEF_RESIZE") = U_SHAPE_LAMALEF_RESIZE;
  m.attr("U_SHAPE_LENGTH_FIXED_SPACES_AT_BEGINNING") = U_SHAPE_LENGTH_FIXED_SPACES_AT_BEGINNING;
  m.attr("U_SHAPE_LENGTH_FIXED_SPACES_AT_END") = U_SHAPE_LENGTH_FIXED_SPACES_AT_END;
  m.attr("U_SHAPE_LENGTH_FIXED_SPACES_NEAR") = U_SHAPE_LENGTH_FIXED_SPACES_NEAR;
  m.attr("U_SHAPE_LENGTH_GROW_SHRINK") = U_SHAPE_LENGTH_GROW_SHRINK;
  m.attr("U_SHAPE_LENGTH_MASK") = U_SHAPE_LENGTH_MASK;

  // Letter shaping options
  m.attr("U_SHAPE_LETTERS_MASK") = U_SHAPE_LETTERS_MASK;
  m.attr("U_SHAPE_LETTERS_NOOP") = U_SHAPE_LETTERS_NOOP;
  m.attr("U_SHAPE_LETTERS_SHAPE_TASHKEEL_ISOLATED") = U_SHAPE_LETTERS_SHAPE_TASHKEEL_ISOLATED;
  m.attr("U_SHAPE_LETTERS_SHAPE") = U_SHAPE_LETTERS_SHAPE;
  m.attr("U_SHAPE_LETTERS_UNSHAPE") = U_SHAPE_LETTERS_UNSHAPE;

  // Presentation form options
  m.attr("U_SHAPE_PRESERVE_PRESENTATION_MASK") = U_SHAPE_PRESERVE_PRESENTATION_MASK;
  m.attr("U_SHAPE_PRESERVE_PRESENTATION_NOOP") = U_SHAPE_PRESERVE_PRESENTATION_NOOP;
  m.attr("U_SHAPE_PRESERVE_PRESENTATION") = U_SHAPE_PRESERVE_PRESENTATION;

  // Seen memory options
  m.attr("U_SHAPE_SEEN_MASK") = U_SHAPE_SEEN_MASK;
  m.attr("U_SHAPE_SEEN_TWOCELL_NEAR") = U_SHAPE_SEEN_TWOCELL_NEAR;

  m.attr("U_SHAPE_SPACES_RELATIVE_TO_TEXT_BEGIN_END") = U_SHAPE_SPACES_RELATIVE_TO_TEXT_BEGIN_END;
  m.attr("U_SHAPE_SPACES_RELATIVE_TO_TEXT_MASK") = U_SHAPE_SPACES_RELATIVE_TO_TEXT_MASK;
  m.attr("U_SHAPE_TAIL_NEW_UNICODE") = U_SHAPE_TAIL_NEW_UNICODE;
  m.attr("U_SHAPE_TAIL_TYPE_MASK") = U_SHAPE_TAIL_TYPE_MASK;

  // Memory options
  m.attr("U_SHAPE_TASHKEEL_BEGIN") = U_SHAPE_TASHKEEL_BEGIN;
  m.attr("U_SHAPE_TASHKEEL_END") = U_SHAPE_TASHKEEL_END;
  m.attr("U_SHAPE_TASHKEEL_MASK") = U_SHAPE_TASHKEEL_MASK;
  m.attr("U_SHAPE_TASHKEEL_REPLACE_BY_TATWEEL") = U_SHAPE_TASHKEEL_REPLACE_BY_TATWEEL;
  m.attr("U_SHAPE_TASHKEEL_RESIZE") = U_SHAPE_TASHKEEL_RESIZE;

  // Direction indicators
  m.attr("U_SHAPE_TEXT_DIRECTION_LOGICAL") = U_SHAPE_TEXT_DIRECTION_LOGICAL;
  m.attr("U_SHAPE_TEXT_DIRECTION_MASK") = U_SHAPE_TEXT_DIRECTION_MASK;
  m.attr("U_SHAPE_TEXT_DIRECTION_VISUAL_LTR") = U_SHAPE_TEXT_DIRECTION_VISUAL_LTR;
  m.attr("U_SHAPE_TEXT_DIRECTION_VISUAL_RTL") = U_SHAPE_TEXT_DIRECTION_VISUAL_RTL;

  // YehHamza memory options
  m.attr("U_SHAPE_YEHHAMZA_MASK") = U_SHAPE_YEHHAMZA_MASK;
  m.attr("U_SHAPE_YEHHAMZA_TWOCELL_NEAR") = U_SHAPE_YEHHAMZA_TWOCELL_NEAR;
}
